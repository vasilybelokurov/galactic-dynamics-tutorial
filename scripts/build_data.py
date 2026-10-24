"""Build the data files for the data chapters (11-13); they are published on Zenodo, not in this repo:
https://doi.org/10.5281/zenodo.23627795 (licence CC BY-NC 4.0; the record's README.md documents every file).

Usage:  python scripts/build_data.py [solar_neighbourhood|halo_gse|disc_giants|rotation_curves|dsph_gaia|all]
        (writes data_build/*.parquet)

Needs access to WSDB (https://wsdb.readthedocs.io, Cambridge) through sqlutilpy. The same tables are
public elsewhere: Gaia DR3 at https://gea.esac.esa.int/archive/ and Andrae, Rix & Chandra 2023 (v2.1)
at https://doi.org/10.5281/zenodo.7945154, so the SQL below can be rerun against those.

Sources
  Gaia DR3 (Gaia Collaboration, Vallenari et al. 2023, https://ui.adsabs.harvard.edu/abs/2023A&A...674A...1G),
      licence CC BY-NC 3.0 IGO.
  Radial velocities corrected for the magnitude trend of Katz et al. 2023, Eq. 5
      (https://ui.adsabs.harvard.edu/abs/2023A&A...674A...5K), for rv_template_teff < 8500 K and grvs_mag >= 11.
  [M/H], Teff, log g from Gaia XP: Andrae, Rix & Chandra 2023 v2.1 table 1
      (https://ui.adsabs.harvard.edu/abs/2023ApJS..267....8A), licence CC BY 4.0. Trained on APOGEE DR17 M_H,
      which equals APOGEE [Fe/H] to ~0.02 dex, so we call it feh. No per-star uncertainties are given.
"""
import io
import sys
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import sqlutilpy as sqlutil

OUT = Path(__file__).resolve().parent.parent / "data_build"

# Columns shared by the Gaia-based files: raw observables and their errors, so that the chapters
# do the transformation to Galactocentric coordinates themselves.
GAIA_COLS = """
    g.source_id, g.ra, g.dec, g.parallax, g.parallax_error,
    g.pmra, g.pmra_error, g.pmdec, g.pmdec_error, g.pmra_pmdec_corr,
    g.radial_velocity - CASE WHEN g.rv_template_teff < 8500 AND g.grvs_mag >= 11
                             THEN 0.02755 * g.grvs_mag ^ 2 - 0.55863 * g.grvs_mag + 2.81129 ELSE 0 END
        AS radial_velocity,
    g.radial_velocity_error, g.phot_g_mean_mag, g.bp_rp, g.ruwe,
    a.mh_xgboost AS feh, a.teff_xgboost AS teff, a.logg_xgboost AS logg, a.in_training_sample
"""

QUERIES = {
    # A cylinder around the Sun: within 0.5 kpc in the plane and 1.2 kpc vertically (distance = 1/parallax),
    # tall enough to hold the outer turns of the phase spiral. Parallax S/N > 10, good astrometry. ~4.6 M stars.
    "solar_neighbourhood": f"""
        SELECT {GAIA_COLS}
        FROM gaia_dr3_aux.gaia_source_rv g
        LEFT JOIN koposov.andrae2023_v21_table1 a ON a.source_id = g.source_id
        WHERE g.radial_velocity IS NOT NULL AND g.parallax > 1 / 1.3 AND g.parallax_over_error > 10
          AND g.ruwe < 1.4
          AND cos(radians(g.b)) / g.parallax < 0.5 AND abs(sin(radians(g.b))) / g.parallax < 1.2""",
    # Metal-poor stars, selected on chemistry only (no kinematic cut), parallax S/N > 5.
    "halo_gse": f"""
        SELECT {GAIA_COLS}
        FROM gaia_dr3_aux.gaia_source_rv g
        JOIN koposov.andrae2023_v21_table1 a ON a.source_id = g.source_id
        WHERE g.radial_velocity IS NOT NULL AND g.parallax_over_error > 5 AND g.ruwe < 1.4
          AND a.mh_xgboost < -1""",
}

# float32 is ample for everything except positions (float64 keeps sub-mas precision) and IDs.
KEEP64 = {"source_id", "ra", "dec"}
# The solar-neighbourhood file is the big one (3.6 M rows), so it is slimmed: positions in float32
# (0.08 arcsec resolution, irrelevant for dynamics) and columns it does not need dropped (RUWE was cut on).
SLIM = {"solar_neighbourhood": dict(keep64={"source_id"},
                                    drop={"ruwe", "pmra_pmdec_corr", "teff", "in_training_sample"})}


def save(name, d):
    keep64, drop = SLIM.get(name, {}).get("keep64", KEEP64), SLIM.get(name, {}).get("drop", set())
    df = pd.DataFrame({k: (v if k in keep64 or v.dtype.kind not in "f" else v.astype(np.float32))
                       for k, v in d.items() if k not in drop})
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{name}.parquet"
    df.to_parquet(path, compression="zstd", index=False)
    print(f"{name}: {len(df):,} rows, {path.stat().st_size / 1e6:.1f} MB -> {path}")
    return df


def fetch(url):
    with urllib.request.urlopen(url, timeout=300) as r:
        return r.read()


# Disc red giants with spectrophotometric parallaxes: Hogg, Eilers & Rix 2019
# (https://ui.adsabs.harvard.edu/abs/2019AJ....158..147H; data https://doi.org/10.5281/zenodo.1468053, CC BY 4.0),
# the stars behind the Eilers et al. 2019 rotation curve. Line-of-sight velocities and abundances from
# APOGEE DR17 (Abdurro'uf et al. 2022), proper motions from Gaia DR3 (APOGEE DR17 lists the Gaia (E)DR3 source_id).
HOGG_URL = "https://zenodo.org/api/records/1468053/files/data_HoggEilersRix2018.fits/content"
# Two steps, because the two joins need opposite plans: apogee_id has no index, so the APOGEE join must be
# a hash join (one pass over allstar), while gaia_source (1.8e9 rows) must be probed through its source_id index.
APOGEE_SQL = """
    SELECT DISTINCT ON (a.apogee_id) h.*, a.vhelio_avg, a.verr, a.vscatter, a.nvisits, a.snr,
           a.teff, a.logg, a.fe_h, a.mg_fe, a.gaiaedr3_source_id AS source_id
    FROM mytab h JOIN apogee_dr17.allstar a ON a.apogee_id = h.apogee_id
    ORDER BY a.apogee_id, a.snr DESC                  -- one row per star: the highest-S/N spectrum"""
GAIA_SQL = """
    SELECT m.source_id, g.ra, g.dec, g.parallax AS gaia_parallax, g.parallax_error AS gaia_parallax_error,
           g.pmra, g.pmra_error, g.pmdec, g.pmdec_error, g.pmra_pmdec_corr, g.ruwe
    FROM mytab m JOIN gaia_dr3.gaia_source g ON g.source_id = m.source_id"""


def build_disc_giants():
    from astropy.table import Table
    t = Table.read(io.BytesIO(fetch(HOGG_URL)))
    names = ["apogee_id", "spec_parallax", "spec_parallax_error", "training_set", "sample"]
    arrays = [np.asarray(t["2MASS_ID"]).astype(str), np.asarray(t["spec_parallax"], float),
              np.asarray(t["spec_parallax_err"], float), np.asarray(t["training_set"], int),
              np.asarray(t["sample"]).astype(str)]
    ap = pd.DataFrame(sqlutil.local_join(APOGEE_SQL, "mytab", arrays, names, asDict=True,
                                         preamb="SET enable_nestloop = off"))
    ap = ap[ap.source_id > 0]                         # NULL source_id comes back as intNullVal = -9999
    ga = pd.DataFrame(sqlutil.local_join(GAIA_SQL, "mytab", [ap.source_id.to_numpy()], ["source_id"],
                                         asDict=True))
    df = ap.merge(ga, on="source_id")
    print(f"Hogg+19: {len(t):,} stars; in APOGEE DR17 with a Gaia id: {len(ap):,}; with Gaia DR3: {len(df):,}")
    return save("disc_giants", {c: df[c].to_numpy() for c in df.columns})


# Published circular-velocity curves, transcribed from the LaTeX tables in the arXiv sources:
# Eilers et al. 2019 Table 1 (https://ui.adsabs.harvard.edu/abs/2019ApJ...871..120E, arXiv:1810.09466) and
# Ou et al. 2024 Table 1 (https://ui.adsabs.harvard.edu/abs/2024MNRAS.528..693O, arXiv:2303.12838).
# Commented-out rows (Eilers' inner points, which they exclude) are skipped.
VC_TABLES = {"Eilers2019": ("1810.09466", "main.tex", ["R", "vc", "vc_err_minus", "vc_err_plus"]),
             "Ou2024": ("2303.12838", "tab01.tex", ["R", "vc", "vc_err_plus", "vc_err_minus", "n_star"])}


def build_rotation_curves():
    rows = []
    for source, (arxiv, fname, cols) in VC_TABLES.items():
        with tarfile.open(fileobj=io.BytesIO(fetch(f"https://arxiv.org/e-print/{arxiv}"))) as tar:
            tex = tar.extractfile(fname).read().decode()
        for line in tex.splitlines():
            vals = line.strip().rstrip("\\").split("&")
            if line.lstrip().startswith("%") or len(vals) != len(cols):
                continue
            try:
                rec = dict(zip(cols, map(float, vals)))
            except ValueError:                     # header rows
                continue
            rows.append({"source": source, **rec})
    df = pd.DataFrame(rows)
    print(df.groupby("source").R.agg(["count", "min", "max"]))
    d = {c: df[c].to_numpy() for c in df.columns}
    return save("rotation_curves", d)


# Dwarf spheroidals: Walker, Mateo & Olszewski 2009 MMFS velocities for Carina, Fornax, Sculptor, Sextans
# (https://ui.adsabs.harvard.edu/abs/2009AJ....137.3100W; VizieR J/AJ/137/3100, doi:10.26093/cds/vizier.51373100).
# The chapter reads that table from VizieR itself; this file adds only the Gaia DR3 counterpart of each star
# (nearest source within 1 arcsec), keyed on Walker's Target id, for proper-motion membership checks.
WALKER_URL = ("https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/137/3100/stars"
              "&-out=Target&-out.add=_RAJ,_DEJ&-out.max=unlimited")   # _RAJ2000, _DEJ2000: decimal degrees
DSPH_SQL = """
    SELECT DISTINCT ON (m.target) m.target, g.source_id, q3c_dist(m.ra, m.dec, g.ra, g.dec) * 3600 AS sep_arcsec,
           g.parallax, g.parallax_error, g.pmra, g.pmra_error, g.pmdec, g.pmdec_error, g.pmra_pmdec_corr,
           g.phot_g_mean_mag, g.bp_rp, g.ruwe
    FROM mytab m JOIN gaia_dr3.gaia_source g ON q3c_join(m.ra, m.dec, g.ra, g.dec, 1. / 3600)
    ORDER BY m.target, sep_arcsec"""


def build_dsph_gaia():
    lines = [l.split("\t") for l in fetch(WALKER_URL).decode().splitlines() if l and not l.startswith("#")]
    col = {name: i for i, name in enumerate(lines[0])}
    rows = lines[3:]                                  # after the header, units and dashes rows
    target = np.array([r[col["Target"]].strip() for r in rows])
    ra = np.array([float(r[col["_RAJ2000"]]) for r in rows])
    dec = np.array([float(r[col["_DEJ2000"]]) for r in rows])
    d = sqlutil.local_join(DSPH_SQL, "mytab", [target, ra, dec], ["target", "ra", "dec"], asDict=True)
    print(f"Walker+09: {len(target):,} stars; with a Gaia DR3 source within 1\": {len(d['target']):,}")
    return save("dsph_gaia", d)


BUILDERS = {**{name: (lambda n=name: save(n, sqlutil.get(QUERIES[n], asDict=True))) for name in QUERIES},
            "disc_giants": build_disc_giants, "rotation_curves": build_rotation_curves,
            "dsph_gaia": build_dsph_gaia}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (BUILDERS if which == "all" else [which]):
        BUILDERS[name]()

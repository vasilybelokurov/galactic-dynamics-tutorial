# STRUCTURE.md

Structure of the tutorial. Audience: self-study students who want to learn
galactic dynamics (not tied to any lecture course). Entry level: Newtonian
mechanics, basic calculus, basic Python/numpy. Exit level: building and
testing equilibrium galaxy models with AGAMA.

## Principles

1. **Analytic target before numerics.** Each chapter states a result students can
   predict, then computes it.
2. **Oracle before black box.** Each AGAMA feature first appears beside an
   analytic or hand-written numpy version, then is used as a black box. Every
   chapter connects back to AGAMA: hand-built chapters end with a "The same with
   AGAMA" section that reproduces their results.
3. **Units.** G = 1 in Ch 1–3 (AGAMA without `setUnits`). Physical units (kpc, km/s, Msun; time
   unit ≈ 0.978 Gyr) from Ch 4 onwards, after one rescaling exercise. Every notebook
   states its units in the first cell. `agama.setUnits` is called before any
   AGAMA object is created (AGAMA manual §3.1).
4. **Plot + assertion.** Every claim comes with a figure and a numerical check.
5. **Synthetic data before real data.**

## Core chapters

| Ch | Title | Learning objective | Check (assertable) |
|---|---|---|---|
| 0 | Setup | Install AGAMA; units (`setUnits`); `Potential`, circular speed from `force`, `agama.orbit` | Plummer Φ(0) = −GM/b; v_c vs formula to 1e-10; energy and J_r conserved |
| 1 | Spherical mass & effective potential | Shell theorem, M(r), V_c, virial theorem; turning points from V_eff (Kepler, homogeneous sphere, Plummer); §1.5 the same with AGAMA (`potential`, `enclosedMass`, `Multipole` from a user density, `Rcirc`, `Rperiapo`) | Kepler roots of E = V_eff give a(1∓e) to 1e-8 a; Plummer V_c peaks at √2 b; AGAMA agrees with hand results |
| 2 | Integrating an orbit | Leapfrog; accuracy vs conservation; RK4 as exercise; §2.7 `agama.orbit` put through the same tests | leapfrog position error ratio e(h)/e(h/2) ∈ [3.5, 4.5]; no secular energy drift; leapfrog − AGAMA difference ∝ h² |
| 3 | Spherical orbits with AGAMA | Rosettes, apsidal angle, radial and azimuthal periods; rescaling to physical units | apsidal angle → π (harmonic) and 2π (Kepler) limits; same orbit in G=1 and physical units agrees after rescaling |
| 4 | Disks & a Milky Way potential | Cylindrical coordinates; exponential disk (Freeman, Bessel functions), Mestel; Miyamoto–Nagai; composite potentials, MWPotential2014 and McMillan17; rotation curve vs Eilers et al. 2019; dark matter | cart→cyl→cart round trip to 1e-12; AGAMA thin disk vs Freeman to 2e-3, peak at 2.15 R_d; MN v_c and F_z to 1e-10; v_c² of components add; v_c(8 kpc) = 220 km/s (MWPotential2014) |
| 5 | Axisymmetric orbits & epicycles | E, L_z, Φ_eff and zero-velocity curve in the meridional plane; third integral, surfaces of section, resonant islands, E_z vs J_z; κ, ν, Ω via `pot.eval(der=True)`; epicycle ellipse; Oort A, B vs Gaia DR1 (Bovy 2017) | E, L_z conserved to 1e-6; J_z constant to <1% while E_z varies >5%; κ/Ω = 1, √2, 2; epicycle frequencies vs orbit and ActionFinder to 0.5%; Y/X = 2Ω/κ, retrograde; A − B = Ω, κ² = −4B(A−B) |
| 6 | Ensembles, CBE, phase mixing | Phase-space density, Liouville/CBE (patch area conserved), angle drift θ = θ₀ + Ω(J)t, coarse-grained f, Jeans theorem, phase spiral as a clock | harmonic patch returns after one period (negative control, 1e-6); isochrone patch area to 1e-5; clumpiness prediction vs ActionFinder to 1e-4; time since kick recovered to 2% |
| 7 | Jeans equations | Spherical Jeans (solver checked vs AGAMA `GalaxyModel.moments`), M(r) from a 3-d sample of a dwarf (Plummer stars in NFW), projection and σ_los, mass–anisotropy degeneracy (NFW fits under wrong β), Wolf estimator, asymmetric drift with a QuasiIsothermal DF | isotropic Plummer σ_r² = GM / [6√(r²+b²)] to 1e-4; projected Jeans vs AGAMA to 2e-3; ⟨σ_los²⟩ independent of β; asymmetric drift vs DF to < 1 km/s |
| 8 | Spherical DFs & sampling | Eddington inversion by hand (Plummer, Hernquist) vs AGAMA `QuasiSpherical`; sampling by hand and with `GalaxyModel.sample`; equilibrium test (Eddington sample vs Gaussian-with-Jeans-σ); Osipkov–Merritt DFs and the r_a ≥ 3b/4 positivity limit. Isothermal sphere and King models not yet covered (candidate optional chapter) | ∫f d³v recovers ρ(r) to 1e-3 (achieved 1e-12); f vs analytic Plummer 1e-6; AGAMA DF agreement 1e-3; Lagrange radii of the Eddington sample constant to 3% over 30 periods |
| 9 | Actions | 1-d action as area and adiabatic invariance (time-varying oscillator); spherical actions by quadrature vs isochrone formula vs AGAMA; Ω = ∂H/∂J; Stäckel fudge accuracy along MW orbits; torus mapping (`ActionMapper`) round trip | isochrone J_r = GM/√(−2E) − ½[L + √(L² + 4GMb)] to 1e-6 (achieved 2e-11 quadrature, 4e-13 AGAMA); Stäckel actions constant to < 1% rms; torus round trip to 0.1% |
| 10 | Action-based DFs & self-consistent models | QuasiIsothermal disk, DoublePowerLaw halo, moments; self-consistent iteration (spherical first) | DF moments recover Plummer σ_r to 1e-3; SCM residual < 1e-3 |
| 11 | Data application | Forward model of a frozen, documented data extract (synthetic mock first) | projection recovers Plummer Σ(R) = Mb² / [π(R²+b²)²] to 1e-4 |

Tolerances are starting budgets; each must be confirmed when the chapter is written.

## Optional chapters

| Ch | Title | Prerequisite |
|---|---|---|
| A1 | Potential expansions (Multipole, CylSpline, convergence in lmax) | 4 |
| A2 | Rotating frames & bars: Jacobi integral, Lagrange points, tidal radius, resonances, Lyapunov exponents | 5 |
| A3 | Time-dependent potentials & tidal streams (LMC–MW exercise) | A2, 9 |
| A4 | Two-body relaxation, dynamical friction, wakes | 8 |
| A5 | Schwarzschild orbit-superposition modelling | 10 |
| A6 | DF inference with selection effects and measurement errors | 10, 11 |

Appendices: special functions (Legendre, Bessel); orbital elements.

## Repository layout

```
notebooks/      NN_<slug>.ipynb, one per chapter (canonical teaching source, committed without outputs)
tests/          pytest tests against analytic results
_config.yml     Jupyter Book 1.0.4.post1 configuration (Colab launch buttons)
_toc.yml        book table of contents; intro.md is the landing page
.github/workflows/agama-wheels.yml   builds ready-made AGAMA wheels (release `agama-wheels`)
.github/workflows/book.yml           tests, executes and publishes the book on every push
```

Each notebook is self-contained, so that it runs in Colab from a single file. A shared package
(`src/galdyn/`) will be added only when later chapters reuse the same code.

## Testing

- `pytest tests/ --nbmake notebooks/`: runs the tests and executes every notebook in a fresh
  kernel (this also isolates `agama.setUnits`). Notebooks contain explicit `assert` cells.
- `jupyter-book build . -W -n --keep-going`: re-executes all notebooks and fails on any warning.
- Both run in CI on every push; the site is published to
  https://vasilybelokurov.github.io/galactic-dynamics-tutorial/
- Fixed random seeds; pinned AGAMA version.

## Online delivery

### Running in the browser

AGAMA is a compiled C++ extension that requires GSL. PyPI ships only a source
distribution (`agama-1.0.0.tar.gz`), so every install compiles.

| Option | Runs where | AGAMA feasible? | Status |
|---|---|---|---|
| Static site (Jupyter Book, pre-executed outputs) | nothing runs; read only | yes | baseline: always provide |
| Google Colab ("Open in Colab" button) | Google VM, browser UI | yes, with the install cell below | TESTED 2026-10-24: ready-made wheel installs in 11 s; smoke test passes |
| Binder (mybinder.org) | free JupyterHub VM | yes: `apt.txt` (libgsl-dev) + `requirements.txt`; image built once and cached | UNVERIFIED |
| JupyterLite / Pyodide (true in-browser WebAssembly) | user's browser | not out of the box: no AGAMA wasm wheel, GSL not in Pyodide, no OpenMP | would need a custom Emscripten build of GSL + AGAMA |

Plan: a Jupyter Book site with pre-executed outputs, plus Colab and Binder launch
buttons on every chapter. Ch 1–2 (numpy only) can also run in JupyterLite.

Colab install cell (tested 2026-10-24 on a fresh Colab runtime: 11 s; see `notebooks/00_setup.ipynb`):

```python
import sys, importlib.util
if importlib.util.find_spec('agama') is None:
    v = f'cp{sys.version_info.major}{sys.version_info.minor}'
    !pip install -q "https://github.com/vasilybelokurov/galactic-dynamics-tutorial/releases/download/agama-wheels/agama-1.0-{v}-{v}-linux_x86_64.whl"
```

- Wheels for Python 3.12 and 3.13 are built by `.github/workflows/agama-wheels.yml` from
  GalacticDynamics-Oxford/Agama@f302756 on Ubuntu 24.04 with GSL linked statically and
  `-march=x86-64-v2`; CI runs `tests/test_agama_smoke.py` before publishing.
- When Colab moves to a new Python version, add it to the workflow matrix and re-run it.
- `pip install agama` from PyPI FAILS on Colab (the 1.0.0 sdist is a 1.3 kB stub). Fallback
  if no wheel matches: `apt-get install libgsl-dev` and
  `pip install --no-build-isolation git+https://github.com/GalacticDynamics-Oxford/Agama.git --config-settings --build-option=--yes`
  (about 6 min).

## Sources

- AGAMA reference manual (Vasiliev): https://github.com/GalacticDynamics-Oxford/Agama/blob/master/doc/reference.pdf
- J. Bovy, *Dynamics and Astrophysics of Galaxies*: https://galaxiesbook.org
- Instructor's SDSG lecture notebooks (local; source of examples)

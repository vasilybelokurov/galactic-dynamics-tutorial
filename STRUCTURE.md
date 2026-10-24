# STRUCTURE.md

Structure of the tutorial. Audience: self-study students who want to learn
galactic dynamics (not tied to any lecture course). Entry level: Newtonian
mechanics, basic calculus, basic Python/numpy. Exit level: building and
testing equilibrium galaxy models with AGAMA.

## Principles

1. **Analytic target before numerics.** Each chapter states a result students can
   predict, then computes it.
2. **Oracle before black box.** Each AGAMA feature first appears beside an
   analytic or hand-written numpy version, then is used as a black box.
3. **Units.** G = 1 and numpy in Ch 1–3. Physical units (kpc, km/s, Msun; time
   unit ≈ 0.978 Gyr) from Ch 4 onwards, after one rescaling exercise. Every notebook
   states its units in the first cell. `agama.setUnits` is called before any
   AGAMA object is created (AGAMA manual §3.1).
4. **Plot + assertion.** Every claim comes with a figure and a numerical check.
5. **Synthetic data before real data.**

## Core chapters

| Ch | Title | Learning objective | Check (assertable) |
|---|---|---|---|
| 0 | Setup & conventions | Run a notebook; units; Cartesian/cylindrical/spherical conventions | cart→cyl→cart round trip of positions and velocities to 1e-12 |
| 1 | Spherical mass & effective potential | Shell theorem, M(r), V_c, virial theorem; turning points from V_eff (Kepler, homogeneous sphere, Plummer) | Kepler roots of E = V_eff give a(1∓e) to 1e-8 a; Plummer V_c peaks at √2 b |
| 2 | Integrating an orbit | Leapfrog; accuracy vs conservation; RK4 as exercise | leapfrog position error ratio e(h)/e(h/2) ∈ [3.5, 4.5]; no secular energy drift |
| 3 | Spherical orbits & first AGAMA | Rosettes, apsidal angle, peri/apocentre; `agama.Potential`, `agama.orbit`; rescaling to physical units | own leapfrog vs `agama.orbit` for Kepler (Plummer with scaleRadius=0); apsidal angle → π (harmonic) and 2π (Kepler) limits |
| 4 | Disks & a Milky Way potential | Mestel, exponential (Bessel functions), Miyamoto–Nagai, composite MW model | MN midplane v_c² = GMR²/[R²+(a+b)²]^{3/2} to 1e-6 |
| 5 | Axisymmetric orbits & epicycles | L_z, Φ_eff in the meridional plane, κ, ν, Ω; Oort A, B; third integral, surfaces of section | κ/Ω = 1 (Kepler), √2 (flat V_c), 2 (homogeneous); A − B = Ω, A + B = −dV_c/dR |
| 6 | Ensembles, CBE, phase mixing | Phase-space density, collisionless Boltzmann equation, Jeans theorem, phase mixing, phase spiral | harmonic-oscillator ensemble returns to start after one period (negative control) |
| 7 | Jeans equations | Spherical Jeans, mass estimators, mass–anisotropy degeneracy, asymmetric drift | isotropic Plummer σ_r² = GM / [6√(r²+b²)] to 1e-4 |
| 8 | Spherical DFs & sampling | Eddington inversion, Plummer, isothermal sphere, King models (+ globular-cluster fit), sampling with `GalaxyModel.sample` | ∫f d³v of the inverted Plummer DF recovers ρ(r) to 1e-3 |
| 9 | Actions | Action-angle variables; isochrone (exact); Stäckel fudge (approximate) | isochrone J_r = GM/√(−2E) − ½[L + √(L² + 4GMb)] to 1e-6 |
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
notebooks/      chNN_<slug>.ipynb, one per chapter (teaching source)
src/galdyn/     reusable functions, organised by responsibility (integrators, potentials, ...)
tests/          pytest tests against analytic results
```

## Testing

- `pytest tests/`: analytic and convergence checks for `src/galdyn`.
- `pytest --nbmake notebooks/`: executes every notebook in a fresh kernel (this also
  isolates `setUnits`). Notebooks contain explicit `assert` cells.
- Fixed random seeds; pinned AGAMA version.

## Online delivery

### Running in the browser

AGAMA is a compiled C++ extension that requires GSL. PyPI ships only a source
distribution (`agama-1.0.0.tar.gz`), so every install compiles.

| Option | Runs where | AGAMA feasible? | Status |
|---|---|---|---|
| Static site (Jupyter Book, pre-executed outputs) | nothing runs; read only | yes | baseline: always provide |
| Google Colab ("Open in Colab" button) | Google VM, browser UI | yes, with the install cell below | TESTED 2026-10-24: builds in 6 min 4 s on 2 cores; smoke test passes |
| Binder (mybinder.org) | free JupyterHub VM | yes: `apt.txt` (libgsl-dev) + `requirements.txt`; image built once and cached | UNVERIFIED |
| JupyterLite / Pyodide (true in-browser WebAssembly) | user's browser | not out of the box: no AGAMA wasm wheel, GSL not in Pyodide, no OpenMP | would need a custom Emscripten build of GSL + AGAMA |

Plan: a Jupyter Book site with pre-executed outputs, plus Colab and Binder launch
buttons on every chapter. Ch 1–2 (numpy only) can also run in JupyterLite.

Colab install cell (tested 2026-10-24; Ubuntu 24.04, Python 3.13.16, 2 CPUs):

```python
!apt-get -qq install -y libgsl-dev
!pip install --no-build-isolation "git+https://github.com/GalacticDynamics-Oxford/Agama.git" --config-settings --build-option=--yes
```

- `pip install agama` from PyPI FAILS on Colab: the PyPI sdist (1.0.0, 1.3 kB) is a
  stub, and its wheel build exits with no output.
- The GitHub build gives AGAMA 1.0.161 with OpenMP, GSL, Eigen and CVXOPT.
- Smoke test on Colab: Φ(0) of a Plummer model equals −GM/b exactly; max |ΔE/E| = 7.4e−7
  over a 10-time-unit orbit; Jr std/mean along the orbit = 3.5e−6; sampling 1e5
  particles took 2.1 s; sampled σ_r² at r ≈ b is 5042 (km/s)² vs analytic 5069 (−0.5%).
- Cost: about 6 min per fresh Colab session. Fix: build a prebuilt Linux wheel (GSL bundled,
  no `-march=native`) and host it on GitHub releases, so the install takes seconds.

## Sources

- AGAMA reference manual (Vasiliev): https://github.com/GalacticDynamics-Oxford/Agama/blob/master/doc/reference.pdf
- J. Bovy, *Dynamics and Astrophysics of Galaxies*: https://galaxiesbook.org
- Instructor's SDSG lecture notebooks (local; source of examples)

# AGENTS.md

## Project

A Python tutorial in Galactic Dynamics that teaches computational dynamics
step by step, starting at beginner level. It uses
[AGAMA](https://github.com/GalacticDynamics-Oxford/Agama)
(Vasiliev 2019, [MNRAS 482, 1525](https://doi.org/10.1093/mnras/sty2672)).

## Rules

1. **Write the least code that works.**
2. **Reproduce every bug with a failing test** before fixing it.
3. **Show a plot before claiming a result.**

## Workflow

- Chapters are `notebooks/NN_<slug>.ipynb`, committed without outputs; each runs standalone in Colab.
- Each notebook backs every claim with a plot and an `assert` against a known result.
- Before pushing: `pytest tests/ --nbmake notebooks/` and `jupyter-book build . -W -n --keep-going`.
- Units: G = 1 in Chapters 1–2; physical units (kpc, km/s, Msun) once AGAMA is introduced.

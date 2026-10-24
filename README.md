# Galactic Dynamics with AGAMA

A step-by-step Python tutorial in computational galactic dynamics, from beginner level
upwards, built on [AGAMA](https://github.com/GalacticDynamics-Oxford/Agama)
(Vasiliev 2019, [MNRAS 482, 1525](https://doi.org/10.1093/mnras/sty2672)).

**Read online:** https://vasilybelokurov.github.io/galactic-dynamics-tutorial/

Status: in development (Chapters 0–12). The planned chapters are in [STRUCTURE.md](STRUCTURE.md).

## Run in the browser

Open any notebook in Google Colab, e.g.
[Chapter 0 — Setup](https://colab.research.google.com/github/vasilybelokurov/galactic-dynamics-tutorial/blob/main/notebooks/00_setup.ipynb).
The first cell installs a ready-made AGAMA wheel from this repository's
[`agama-wheels` release](https://github.com/vasilybelokurov/galactic-dynamics-tutorial/releases/tag/agama-wheels)
(built by [`.github/workflows/agama-wheels.yml`](.github/workflows/agama-wheels.yml) from the upstream AGAMA source).

## Run locally

Install AGAMA following its [INSTALL](https://github.com/GalacticDynamics-Oxford/Agama/blob/master/INSTALL) notes, then

```bash
pip install -r requirements.txt jupyter pytest nbmake
pytest tests/ --nbmake notebooks/
jupyter lab notebooks/
```

## Licence

Tutorial code and text: MIT (see [LICENSE](LICENSE)). AGAMA is distributed under its own
licence (GPL because it links GSL; AGAMA's own code BSD/MIT) — see the
[AGAMA repository](https://github.com/GalacticDynamics-Oxford/Agama/blob/master/LICENSE).

# Galactic Dynamics with AGAMA

A step-by-step tutorial in computational galactic dynamics, from beginner level upwards.
It uses Python, `numpy`, and the [AGAMA](https://github.com/GalacticDynamics-Oxford/Agama)
library (Vasiliev 2019, [MNRAS 482, 1525](https://doi.org/10.1093/mnras/sty2672)).

**Who it is for.** Students who are interested in galactic dynamics and want to understand it
by experimenting hands-on.

**How to use it.** Every chapter is a Jupyter notebook. Read it here, or press the
rocket icon at the top of a chapter and choose **Colab** to run it in your browser — nothing
to install. Each chapter ends with exercises.

**How it is built.** Every claim is backed by a plot and by a numerical check (`assert`)
against a known result. The notebooks are executed afresh each time this site is built.

| Chapter | Topic |
|---|---|
| 0 | Setup: installing AGAMA and checking it works |
| 1 | Spherical mass, circular speed and the effective potential |
| 2 | Integrating an orbit: Euler, leapfrog, convergence and conservation |
| 3 | Spherical orbits with AGAMA: radial period, apsidal angle, frequencies, physical units |

More chapters are planned — see the
[structure](https://github.com/vasilybelokurov/galactic-dynamics-tutorial/blob/main/STRUCTURE.md).

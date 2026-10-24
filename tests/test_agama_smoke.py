"""Smoke test: AGAMA is installed and reproduces analytic Plummer-model results.

Run: pytest tests/test_agama_smoke.py   (or: python tests/test_agama_smoke.py)
"""
import numpy as np
import agama

agama.setUnits(mass=1, length=1, velocity=1)  # Msun, kpc, km/s
M, B = 1e10, 1.0
POT = agama.Potential(type='Plummer', mass=M, scaleRadius=B)


def test_central_potential():
    # Phi(0) = -G M / b
    assert abs(POT.potential([0, 0, 0]) / (-agama.G * M / B) - 1) < 1e-12


def test_orbit_energy_and_action_conserved():
    _, traj = agama.orbit(potential=POT, ic=[1, 0, 0, 0, 150, 30], time=10.0, trajsize=2001)
    E = POT.potential(traj[:, :3]) + 0.5 * np.sum(traj[:, 3:]**2, axis=1)
    assert np.max(np.abs(E / E[0] - 1)) < 1e-5
    Jr = agama.ActionFinder(POT)(traj[::200])[:, 0]
    assert np.std(Jr) / np.mean(Jr) < 1e-4


def test_sampled_velocity_dispersion():
    # isotropic Plummer: sigma_r^2(r) = G M / (6 sqrt(r^2 + b^2))
    df = agama.DistributionFunction(type='QuasiSpherical', potential=POT, density=POT)
    np.random.seed(42)
    xv, m = agama.GalaxyModel(POT, df).sample(100000)
    assert abs(m.sum() / M - 1) < 1e-2  # DF mass comes from numerical quadrature (0.24% off in AGAMA 1.0.152)
    r = np.linalg.norm(xv[:, :3], axis=1)
    sel = (r > 0.9) & (r < 1.1)
    vr = np.sum(xv[sel, :3] * xv[sel, 3:], axis=1) / r[sel]
    expected = agama.G * M / (6 * np.sqrt(1 + B**2))
    assert abs(np.var(vr) / expected - 1) < 0.03


if __name__ == '__main__':
    for name, f in list(globals().items()):
        if name.startswith('test_'):
            f()
            print('PASS', name)

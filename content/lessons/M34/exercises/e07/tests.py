import numpy as np
import sub


def test_histogram_matches():
    e = sub.sample_cov_eigs(1600, 400, np.random.default_rng(0))
    hist, edges = np.histogram(e, bins=12, range=(0.25, 2.25), density=True)
    mids = (edges[:-1] + edges[1:]) / 2
    assert np.max(np.abs(hist - sub.mp_density(mids, 0.25))) < 0.12
    a, b = sub.mp_edges(0.25)
    assert abs(e[0] - a) < 0.05 and abs(e[-1] - b) < 0.1


def test_moments():
    e = sub.sample_cov_eigs(2000, 500, np.random.default_rng(1))
    m1, m2 = sub.mp_moments(0.25)
    assert abs(e.mean() - m1) < 0.01 and abs(np.mean(e**2) - m2) < 0.03
    x = np.linspace(0.0, 3.0, 300001)
    f = sub.mp_density(x, 0.5)
    assert abs(np.sum((f[1:] + f[:-1]) / 2 * np.diff(x)) - 1) < 1e-3

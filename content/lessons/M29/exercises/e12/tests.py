import numpy as np
import sub


def test_matches_formula():
    rng = np.random.default_rng(12)
    for eta, B in ((0.1, 1), (0.05, 1), (0.1, 8), (1.5, 1)):
        x = sub.simulate(eta, 1.0, 2.0, B, 40000, 400, rng)
        v = sub.stationary_variance(eta, 1.0, 2.0, B)
        assert abs(x.var() / v - 1) < 0.04, (eta, B, x.var(), v)


def test_scalings():
    v = sub.stationary_variance(0.01, 1.0, 1.0, 1)
    assert abs(sub.stationary_variance(0.005, 1.0, 1.0, 1) / v - 0.5) < 0.01
    assert abs(sub.stationary_variance(0.01, 1.0, 1.0, 2) / v - 0.5) < 1e-12

import numpy as np
import sub


def test_ito():
    rng = np.random.default_rng(0)
    n = 200000
    W = np.concatenate([[0.0], np.cumsum(rng.standard_normal(n) * np.sqrt(1.0 / n))])
    assert abs(sub.quadratic_variation(W) - 1) < 0.01
    assert abs(sub.ito_sum(W) - 0.5 * (W[-1] ** 2 - 1)) < 0.01
    assert abs(sub.midpoint_sum(W) - 0.5 * W[-1] ** 2) < 1e-9

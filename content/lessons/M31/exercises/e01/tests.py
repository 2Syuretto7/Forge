import math
import numpy as np
import sub


def test_puzzle():
    assert abs(sub.hoeffding_epsilon(1000, 0.05) - 0.04295) < 1e-4
    assert sub.hoeffding_n(0.01, 0.05) == 18445
    assert abs(sub.hoeffding_epsilon(100, 0.05, -1, 1) - 2 * math.sqrt(math.log(40) / 200)) < 1e-12


def test_bound_holds():
    rng = np.random.default_rng(1)
    for p in (0.1, 0.5, 0.92):
        means = rng.binomial(200, p, size=20000) / 200
        for eps in (0.05, 0.08):
            assert np.mean(np.abs(means - p) >= eps) <= sub.hoeffding_bound(200, eps)
    assert sub.hoeffding_bound(1, 0.01) == 1.0

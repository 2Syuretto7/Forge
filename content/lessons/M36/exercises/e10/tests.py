import numpy as np
import sub


def test_variances_match_theory():
    t = sub.variance_table([1, 4, 16, 64, 256], 10000, np.random.default_rng(0))
    for d, measured in t.items():
        for m, th in zip(measured, sub.theory(d)):
            assert abs(m / th - 1) < 0.15, (d, m, th)
    assert t[256][0] / t[256][2] > 1e4

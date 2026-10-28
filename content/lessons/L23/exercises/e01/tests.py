import numpy as np
import sub

rng = np.random.default_rng(0)
c = (rng.random(400) < 0.7).astype(float)


def test_interval():
    acc, lo, hi = sub.accuracy_ci(c)
    assert acc == c.mean() and lo < acc < hi
    se = sub.standard_error(acc, len(c))
    assert abs((hi - lo) / (2 * 1.96 * se) - 1) < 0.15
    assert abs(sub.standard_error(0.5, 100) - 0.05) < 1e-12

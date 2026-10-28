import numpy as np
import sub

rng = np.random.default_rng(5)
a = rng.normal(1.0, 0.5, 400)
b = a - 0.03 + rng.normal(0, 0.03, 400)


def test_mean_with_ci():
    m, lo, hi = sub.mean_with_ci(a)
    assert abs(m - a.mean()) < 1e-12 and lo < m < hi
    se = a.std() / np.sqrt(len(a))
    assert abs((hi - lo) / (2 * 1.96 * se) - 1) < 0.15


def test_paired_difference_is_precise():
    m, lo, hi = sub.paired_difference(a, b)
    assert 0 < lo < m < hi
    _, alo, ahi = sub.mean_with_ci(a)
    _, blo, bhi = sub.mean_with_ci(b)
    assert alo < bhi and blo < ahi

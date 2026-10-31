import numpy as np
import sub


def test_pass_at_k():
    assert abs(sub.pass_at_k(10, 3, 1) - 0.3) < 1e-12
    assert abs(sub.pass_at_k(10, 3, 2) - (1 - 21 / 45)) < 1e-12
    assert sub.pass_at_k(10, 3, 8) == 1.0 and sub.pass_at_k(10, 0, 3) == 0.0
    assert abs(sub.pass_at_k(200, 50, 10) - 0.94791) < 1e-5


def test_ci():
    s = (np.random.default_rng(0).random(300) < 0.6).astype(float)
    m, lo, hi = sub.mean_ci(s)
    se = np.sqrt(m * (1 - m) / 300)
    assert m == s.mean() and lo < m < hi and abs((hi - lo) / (2 * 1.96 * se) - 1) < 0.15

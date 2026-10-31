import numpy as np
import sub


def test_concentration():
    rng = np.random.default_rng(0)
    for d in (10, 100, 1000):
        m, s = sub.norm_stats(d, 4000, rng)
        assert abs(m - 1) < 0.05 and abs(s - 1 / np.sqrt(2)) < 0.06, (d, m, s)
    assert sub.shell_fraction(1000, 4000, rng) > 0.99
    assert sub.shell_fraction(2, 4000, rng) < 0.2

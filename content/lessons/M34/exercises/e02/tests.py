import numpy as np
import sub


def test_puzzle():
    a = sub.angles_degrees(4096, 2000, np.random.default_rng(0))
    assert abs(a.mean() - 90) < 0.1
    assert abs(a.std() / sub.predicted_angle_sd(4096) - 1) < 0.08
    assert np.max(np.abs(a - 90)) < 5


def test_variance_is_one_over_d():
    rng = np.random.default_rng(1)
    for d in (16, 256):
        c = sub.cosines(d, 20000, rng)
        assert abs(c.var() * d - 1) < 0.05
    low = sub.angles_degrees(3, 20000, rng)
    assert np.mean(np.abs(low - 90) > 30) > 0.4

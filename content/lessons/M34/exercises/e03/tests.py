import numpy as np
import sub


def test_variance_grows_with_d():
    rng = np.random.default_rng(0)
    ratios = sub.variance_ratio([16, 64, 256, 1024], 8000, rng)
    assert all(abs(r - 1) < 0.07 for r in ratios), ratios
    for d in (16, 1024):
        assert abs(sub.score_variance(d, 8000, rng, True) - 1) < 0.07

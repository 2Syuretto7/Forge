import numpy as np
import sub


def test_he_preserves():
    rng = np.random.default_rng(0)
    n = 512
    x = rng.standard_normal((256, n)) * 1.7
    W = rng.standard_normal((n, n)) * np.sqrt(sub.he_variance(n))
    mx, my, mr = sub.layer_second_moments(x, W)
    assert abs(my / (n * sub.he_variance(n) * mx) - 1) < 0.05
    assert abs(mr / mx - sub.relu_gain(n, sub.he_variance(n))) < 0.05
    assert sub.relu_gain(n, sub.xavier_variance(n)) == 0.5


def test_other_scales():
    rng = np.random.default_rng(1)
    x = rng.standard_normal((256, 300))
    for v in (0.5 / 300, 4 / 300):
        W = rng.standard_normal((300, 300)) * np.sqrt(v)
        mx, _, mr = sub.layer_second_moments(x, W)
        assert abs(mr / mx / sub.relu_gain(300, v) - 1) < 0.06

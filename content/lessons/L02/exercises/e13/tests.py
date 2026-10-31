import numpy as np
import sub


def test_error_falls_with_data():
    c = sub.learning_curve([20, 40, 80, 160, 320], 7, 0.3, 200, 0)
    assert np.all(np.diff(c) < 0), c


def test_variance_regime_scales_like_one_over_n():
    c = sub.learning_curve([100, 400], 7, 0.3, 300, 1)
    assert 3 < c[0] / c[1] < 5.5, c[0] / c[1]

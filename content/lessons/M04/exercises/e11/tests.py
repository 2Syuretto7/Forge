import numpy as np
import sub


def test_fit_slope():
    assert abs(sub.fit_slope([0, 1, 2, 3], [1, 3, 5, 7]) - 2) < 1e-12


def test_smooth_curves_have_exponent_two():
    for f, a, b in [(lambda x: np.exp(-x * x), -3, 3), (np.sin, 0, 6), (lambda x: x ** 3, -1, 1)]:
        p = sub.error_exponent(f, a, b, [8, 16, 32, 64, 128])
        assert 1.8 < p < 2.2, p

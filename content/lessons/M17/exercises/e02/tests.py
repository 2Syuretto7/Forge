import math
import numpy as np
import sub


def test_exact_for_cubics():
    assert abs(sub.simpson(lambda x: x ** 3 - 2 * x + 1, 0, 2, 2) - (4 - 4 + 2)) < 1e-12


def test_order_four():
    r = sub.simpson_error_ratio(np.sin, 0, math.pi, 2.0, 16)
    assert 15 < r < 17
    assert abs(sub.simpson(np.sin, 0, math.pi, 204) - 2) < 1e-8


def test_odd():
    try:
        sub.simpson(np.sin, 0, 1, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

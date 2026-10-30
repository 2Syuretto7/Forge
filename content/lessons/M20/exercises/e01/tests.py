import math
import numpy as np
import sub


def test_rectangle():
    assert abs(sub.midpoint_2d(lambda x, y: x * y, 0, 1, 0, 2, 200) - 1) < 1e-4
    assert abs(sub.iterated(lambda x, y: x * y, 0, 1, 0, 2) - 1) < 1e-12
    g = lambda x, y: np.exp(-(x * x + y * y))  # noqa: E731
    assert abs(sub.iterated(g, -6, 6, -6, 6) - math.pi) < 1e-9


def test_triangle():
    assert abs(sub.over_triangle(lambda x, y: np.ones_like(y)) - 0.5) < 1e-12
    assert abs(sub.over_triangle(lambda x, y: x * y) - 1 / 8) < 1e-12

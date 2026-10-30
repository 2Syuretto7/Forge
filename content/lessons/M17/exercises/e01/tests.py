import math
import numpy as np
import sub


def test_values():
    assert abs(sub.riemann(lambda x: x * x, 0, 1, 10, "right") - 0.385) < 1e-12
    assert abs(sub.trapezoid(np.sin, 0, math.pi, 1000) - 2) < 2e-6


def test_orders():
    left = lambda f, a, b, n: sub.riemann(f, a, b, n, "left")  # noqa: E731
    mid = lambda f, a, b, n: sub.riemann(f, a, b, n, "mid")  # noqa: E731
    assert abs(sub.observed_order(left, np.exp, 0, 1, math.e - 1, 64) - 1) < 0.05
    assert abs(sub.observed_order(mid, np.exp, 0, 1, math.e - 1, 64) - 2) < 0.05
    assert abs(sub.observed_order(sub.trapezoid, np.exp, 0, 1, math.e - 1, 64) - 2) < 0.05

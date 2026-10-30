import math
import numpy as np
import sub


def test_disc_and_gaussian():
    assert abs(sub.integrate_polar(lambda x, y: np.ones_like(x), 1.0) - math.pi) < 1e-12
    assert abs(sub.integrate_polar(lambda x, y: np.exp(-(x * x + y * y)), 6.0) - math.pi) < 1e-4
    assert abs(sub.integrate_polar(lambda x, y: x * x + y * y, 1.0) - math.pi / 2) < 1e-5

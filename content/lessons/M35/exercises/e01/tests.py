import math
import numpy as np
import sub


def test_power_law():
    assert abs(sub.loglog_slope(1, sub.power_law(1, 3, 0.4), 50, sub.power_law(50, 3, 0.4)) + 0.4) < 1e-12
    assert abs(sub.scale_factor(0.3, 10) - 10**-0.3) < 1e-15
    assert 0.49 < sub.scale_factor(0.3, 10) < 0.51


def test_scale_invariance():
    xs = [1.0, 7.0, 300.0]
    assert sub.is_scale_invariant(lambda x: 2.5 * x**-0.34, xs, 10)
    assert not sub.is_scale_invariant(lambda x: math.exp(-x / 100), xs, 10)
    assert np.allclose(sub.power_law([1, 10], 2, 1), [2, 0.2])

import math
import sub


def test_sin():
    t = sub.trapezoid_strips(1.0, math.pi, 1e-8)
    s = sub.simpson_strips(1.0, math.pi, 1e-8)
    assert 15000 < t < 17000
    assert s == 116
    assert sub.strips_needed(1.0, 2, 1e-8) == 10000

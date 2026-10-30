import math
import sub


def test_renormalize():
    c, s = sub.renormalize(0.799, 0.602)
    assert abs(c * c + s * s - 1) < 1e-15


def test_length_is_kept():
    c, s = round(math.cos(math.radians(37)), 3), round(math.sin(math.radians(37)), 3)
    x, y = sub.turn_with_renormalization(c, s, 10000)
    assert abs(math.hypot(x, y) - 1) < 1e-10


def test_angle_error_remains():
    c, s = round(math.cos(math.radians(37)), 3), round(math.sin(math.radians(37)), 3)
    e = sub.angle_error(c, s, math.radians(37))
    assert 1e-6 < e < 1e-3

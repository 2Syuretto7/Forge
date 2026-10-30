import math
import sub


def test_exact_rotation_keeps_length():
    c, s = math.cos(0.7), math.sin(0.7)
    assert abs(sub.radius_after(c, s, 10000) - 1) < 1e-10


def test_rounded_rotation_grows():
    c, s = sub.rounded_rotation(math.radians(37), 3)
    f = sub.scale_factor(c, s)
    assert abs(f - 1) > 1e-4
    r = sub.radius_after(c, s, 10000)
    assert abs(r / sub.predicted_radius(c, s, 10000) - 1) < 1e-9
    assert r > 40, r

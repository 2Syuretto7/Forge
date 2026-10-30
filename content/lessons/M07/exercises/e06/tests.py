import math
import random
import sub


def test_against_math():
    rnd = random.Random(0)
    for _ in range(3000):
        a, b = rnd.uniform(-10, 10), rnd.uniform(-10, 10)
        assert abs(sub.cos_sum(a, b) - math.cos(a + b)) < 1e-12
        assert abs(sub.sin_sum(a, b) - math.sin(a + b)) < 1e-12


def test_double_and_half():
    c, s = sub.double_angle(math.pi / 6)
    assert abs(c - 0.5) < 1e-15 and abs(s - math.sqrt(3) / 2) < 1e-15
    for a in [0.0, 0.7, math.pi / 2, math.pi]:
        assert abs(sub.half_angle_cos(a) - math.cos(a / 2)) < 1e-12

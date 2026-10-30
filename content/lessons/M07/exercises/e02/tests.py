import math
import random
import sub


def test_values():
    x, y = sub.point_on_circle(math.pi / 6)
    assert abs(x - math.sqrt(3) / 2) < 1e-15 and abs(y - 0.5) < 1e-15
    assert abs(sub.angle_of(-1, 0) - math.pi) < 1e-15
    assert abs(sub.angle_of(0, -2) + math.pi / 2) < 1e-15
    assert sub.distance((1, 2), (4, 6)) == 5


def test_invariant_angle_and_radius():
    rnd = random.Random(1)
    for _ in range(3000):
        t, r = rnd.uniform(-math.pi + 1e-9, math.pi), rnd.uniform(0.1, 10)
        x, y = sub.point_on_circle(t, r)
        assert abs(sub.angle_of(x, y) - t) < 1e-9
        assert abs(sub.distance((0, 0), (x, y)) - r) < 1e-9

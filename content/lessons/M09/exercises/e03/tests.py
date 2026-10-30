import math
import random
import sub


def test_two_ways_agree():
    rnd = random.Random(0)
    for _ in range(2000):
        x = (rnd.uniform(-5, 5), rnd.uniform(-5, 5))
        y = (rnd.uniform(-5, 5), rnd.uniform(-5, 5))
        assert abs(sub.dot_by_angle(x, y) - (x[0] * y[0] + x[1] * y[1])) < 1e-9


def test_angle():
    assert abs(sub.angle_2d((1, 0), (-1, 0.0001)) - math.pi) < 1e-3
    assert abs(sub.angle_2d((1, 1), (1, -1)) - math.pi / 2) < 1e-12


def test_law_of_cosines():
    rnd = random.Random(1)
    for _ in range(500):
        d = rnd.randint(1, 50)
        x = [rnd.gauss(0, 1) for _ in range(d)]
        y = [rnd.gauss(0, 1) for _ in range(d)]
        assert abs(sub.law_of_cosines_gap(x, y)) < 1e-9

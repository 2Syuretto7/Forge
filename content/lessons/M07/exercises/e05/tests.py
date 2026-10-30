import math
import random
import sub


def test_agree():
    rnd = random.Random(0)
    for _ in range(1000):
        p = (rnd.uniform(-5, 5), rnd.uniform(-5, 5))
        t = rnd.uniform(-10, 10)
        a, b = sub.rotate_complex(p, t), sub.rotate_trig(p, t)
        assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12


def test_compose():
    assert abs(sub.compose_angles([math.radians(30), math.radians(45)]) - math.radians(75)) < 1e-12


def test_quarter_turns():
    assert sub.quarter_turns((3, 4), 1) == (-4, 3)
    assert sub.quarter_turns((3, 4), 2) == (-3, -4)
    assert sub.quarter_turns((3, 4), 4) == (3, 4)

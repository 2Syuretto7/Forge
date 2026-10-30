import math
import random
import sub


def test_cube_root():
    assert abs(sub.inverse(lambda x: x ** 3, 27, 0, 10) - 3) < 1e-9
    cbrt = sub.make_inverse(lambda x: x ** 3, -10, 10)
    assert abs(cbrt(-8) + 2) < 1e-9


def test_unbracketed_raises():
    try:
        sub.inverse(lambda x: x, 20, 0, 10)
    except ValueError:
        return
    raise AssertionError("20 is not between f(0) and f(10)")


def test_invariant_round_trip():
    rnd = random.Random(0)
    fs = [lambda x: x ** 3 + x, math.exp, lambda x: 2 * x - 7, math.atan, lambda x: x + math.sin(x) / 2]
    for f in fs:
        for _ in range(200):
            x = rnd.uniform(-3, 3)
            back = sub.inverse(f, f(x), -4, 4)
            assert abs(back - x) < 1e-9, (x, back)
            assert abs(f(back) - f(x)) < 1e-9

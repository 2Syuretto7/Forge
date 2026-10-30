import math
import random
import sub

sq = lambda x: x * x


def test_shift_and_stretch():
    g = sub.shift(sq, 3, 1)
    assert g(3) == 1 and g(4) == 2
    s = sub.stretch(sq, 2, 3)
    assert s(2) == 3 and s(4) == 12
    assert sub.vertex_after_shift(3, 1) == (3, 1)


def test_reflections():
    g = sub.shift(sq, 3, 1)
    assert sub.reflect_y(g)(-3) == 1
    assert sub.reflect_x(g)(3) == -1


def test_invariant_two_shifts_are_one():
    rnd = random.Random(0)
    for f in [sq, math.sin, math.exp, abs]:
        for _ in range(200):
            h1, k1, h2, k2, x = (rnd.uniform(-2, 2) for _ in range(5))
            a = sub.shift(sub.shift(f, h1, k1), h2, k2)(x)
            b = sub.shift(f, h1 + h2, k1 + k2)(x)
            assert abs(a - b) <= 1e-9 * max(1, abs(b))

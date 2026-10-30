import math
import sub

GRID = [i / 10 for i in range(-30, 31)]


def test_collisions():
    a, b = sub.find_collision(lambda x: x * x, GRID)
    assert a != b and abs(a * a - b * b) < 1e-9
    assert sub.find_collision(lambda x: x ** 3, GRID) is None
    assert not sub.is_injective_on(abs, GRID)
    assert sub.is_injective_on(math.exp, GRID)


def test_largest_injective_interval():
    assert sub.largest_injective_interval(lambda x: x * x, GRID) in [(-3.0, 0.0), (0.0, 3.0)]
    assert sub.largest_injective_interval(lambda x: x ** 3 - 3 * x, GRID) in [(-3.0, -1.0), (-1.0, 1.0), (1.0, 3.0)]
    assert sub.largest_injective_interval(math.exp, GRID) == (-3.0, 3.0)

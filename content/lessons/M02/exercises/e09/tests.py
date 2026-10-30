import random
import sub


def test_example():
    assert sub.complete_square(1, 6, 5) == (3, -4)
    assert sub.vertex(1, 6, 5) == (-3, -4)
    assert sub.minimum_value(2, -8, 3) == -5


def test_matches_the_quadratic_everywhere():
    rnd = random.Random(4)
    for _ in range(200):
        a = rnd.choice([-1, 1]) * rnd.uniform(0.5, 5)
        b, c = rnd.uniform(-5, 5), rnd.uniform(-5, 5)
        h, k = sub.complete_square(a, b, c)
        for _ in range(5):
            x = rnd.uniform(-10, 10)
            assert abs(a * (x + h) ** 2 + k - (a * x * x + b * x + c)) < 1e-9 * (1 + abs(a * x * x))


def test_no_minimum_for_downward_parabola():
    try:
        sub.minimum_value(-1, 0, 0)
    except ValueError:
        return
    raise AssertionError("a < 0 has no minimum")

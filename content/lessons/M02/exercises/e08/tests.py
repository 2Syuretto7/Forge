import random
import sub


def test_examples():
    assert sub.solve_quadratic(1, -10, 21) == [3, 7]
    assert sub.solve_quadratic(1, 6, 5) == [-5, -1]
    assert sub.solve_quadratic(1, -2, 1) == [1]
    assert sub.solve_quadratic(1, 0, 1) == []
    assert sub.discriminant(1, -10, 21) == 16


def test_linear_is_rejected():
    try:
        sub.solve_quadratic(0, 2, 1)
    except ValueError:
        return
    raise AssertionError("a = 0 should raise ValueError")


def test_invariant_roots_are_roots():
    rnd = random.Random(2)
    for _ in range(5000):
        a = rnd.choice([-1, 1]) * rnd.uniform(0.1, 10)
        b, c = rnd.uniform(-10, 10), rnd.uniform(-10, 10)
        roots = sub.solve_quadratic(a, b, c)
        assert roots == sorted(roots)
        assert len(roots) == (2 if b * b - 4 * a * c > 0 else 0 if b * b - 4 * a * c < 0 else 1)
        for r in roots:
            size = abs(a * r * r) + abs(b * r) + abs(c)
            assert abs(a * r * r + b * r + c) <= 1e-9 * size

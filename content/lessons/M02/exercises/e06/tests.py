import random
import sub


def test_example():
    x, y = sub.solve_2x2(1, 1, 1, -1, 10, 4)
    assert abs(x - 7) < 1e-12 and abs(y - 3) < 1e-12


def test_dependent_equations_raise():
    try:
        sub.solve_2x2(2, 4, 1, 2, 6, 3)
    except ValueError:
        return
    raise AssertionError("2x + 4y = 6 and x + 2y = 3 are not independent")


def test_invariant_residual_is_tiny():
    rnd = random.Random(0)
    for _ in range(5000):
        a, b, c, d, p, q = (rnd.uniform(-5, 5) for _ in range(6))
        if abs(a * d - b * c) < 1e-3:
            continue
        x, y = sub.solve_2x2(a, b, c, d, p, q)
        scale = max(1, abs(x), abs(y)) * 10
        assert sub.residual(a, b, c, d, p, q, x, y) < 1e-12 * scale * 1e3


def test_residual():
    assert sub.residual(1, 1, 1, -1, 10, 4, 7, 3) == 0
    assert sub.residual(1, 1, 1, -1, 10, 4, 7, 4) == 1

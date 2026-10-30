import random
import sub


def test_examples():
    assert sub.solve_inequality(2, 1, 7) == ("<", 3)
    assert sub.solve_inequality(-2, 0, 6) == (">", -3)
    assert sub.solve_inequality(0, 1, 2) == "all"
    assert sub.solve_inequality(0, 2, 1) is None
    assert sub.abs_interval(3, 2) == (1, 5)
    assert sub.abs_interval(3, 0) is None


def test_answers_agree_with_points():
    rnd = random.Random(1)
    for _ in range(2000):
        a, b, c, x = rnd.uniform(-5, 5), rnd.uniform(-5, 5), rnd.uniform(-5, 5), rnd.uniform(-20, 20)
        sol = sub.solve_inequality(a, b, c)
        op, bound = sol
        if abs(x - bound) < 1e-9:
            continue
        predicted = x < bound if op == "<" else x > bound
        assert predicted == sub.satisfies(a, b, c, x), (a, b, c, x, sol)

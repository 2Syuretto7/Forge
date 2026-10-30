import random
import sub


def ev(e, env):
    if isinstance(e, str):
        return env[e]
    if not isinstance(e, tuple):
        return e
    op, a, b = e
    x, y = ev(a, env), ev(b, env)
    return {"+": lambda: x + y, "-": lambda: x - y, "*": lambda: x * y, "/": lambda: x / y, "^": lambda: x ** y}[op]()


def test_rules():
    assert sub.simplify(("+", 2, 3)) == 5
    assert sub.simplify(("+", "x", 0)) == "x"
    assert sub.simplify(("*", 1, ("+", "y", 0))) == "y"
    assert sub.simplify(("*", ("+", "x", 1), 0)) == 0
    assert sub.simplify(("-", ("+", "x", 1), ("+", "x", 1))) == 0
    assert sub.simplify(("^", ("*", "x", 1), 1)) == "x"
    assert sub.simplify(("+", ("*", 2, 3), "x")) == ("+", 6, "x")


def random_expr(rnd, d):
    if d == 0 or rnd.random() < 0.25:
        return rnd.choice(["x", "y", 0, 1, 2, 3])
    op = rnd.choice(["+", "-", "*", "/", "^"])
    if op == "^":
        return ("^", random_expr(rnd, d - 1), rnd.choice([0, 1, 2]))
    return (op, random_expr(rnd, d - 1), random_expr(rnd, d - 1))


def test_invariant_simplify_keeps_the_value():
    rnd = random.Random(3)
    checked = 0
    for _ in range(2000):
        e = random_expr(rnd, 4)
        s = sub.simplify(e)
        env = {"x": rnd.uniform(0.5, 3), "y": rnd.uniform(0.5, 3)}
        try:
            v = ev(e, env)
        except (ZeroDivisionError, OverflowError):
            continue
        assert abs(ev(s, env) - v) <= 1e-9 * max(1, abs(v)), (e, s)
        checked += 1
    assert checked > 1000

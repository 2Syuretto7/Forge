import random


# provided
def evaluate(expr, env):
    """Value of expr (number, name, or (op, left, right)) with variables from env."""
    if isinstance(expr, str):
        return env[expr]
    if not isinstance(expr, tuple):
        return expr
    op, a, b = expr
    x, y = evaluate(a, env), evaluate(b, env)
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    if op == "*":
        return x * y
    if op == "/":
        return x / y
    return x ** y


def counterexample(e1, e2, names, trials=200, seed=0):
    """First random point where e1 and e2 disagree, or None."""
    rnd = random.Random(seed)
    for _ in range(trials):
        env = {v: rnd.uniform(-10, 10) for v in names}
        try:
            a, b = evaluate(e1, env), evaluate(e2, env)
        except ZeroDivisionError:
            continue
        if abs(a - b) > 1e-9 * max(1, abs(a)):
            return env
    return None


def same_function(e1, e2, names, trials=50, seed=0):
    """True when e1 and e2 agree at every random point where both are defined."""
    return counterexample(e1, e2, names, trials, seed) is None

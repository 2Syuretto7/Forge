import random

# (a + b)^2 - (a - b)^2, simplified in six steps; two steps are wrong.
CHAIN = [
    ("-", ("^", ("+", "a", "b"), 2), ("^", ("-", "a", "b"), 2)),
    ("-", ("+", ("+", ("^", "a", 2), ("*", ("*", 2, "a"), "b")), ("^", "b", 2)), ("^", ("-", "a", "b"), 2)),
    ("-", ("+", ("+", ("^", "a", 2), ("*", ("*", 2, "a"), "b")), ("^", "b", 2)), ("+", ("^", "a", 2), ("^", "b", 2))),
    ("-", ("+", ("^", "a", 2), ("*", ("*", 2, "a"), "b")), ("^", "a", 2)),
    ("*", ("*", 2, "a"), "b"),
    ("*", ("*", 4, "a"), "b"),
]
NAMES = ["a", "b"]


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


def bad_steps(chain, names, trials=50, seed=0):
    """Indices i where chain[i] differs as a function from chain[i - 1]."""
    raise NotImplementedError

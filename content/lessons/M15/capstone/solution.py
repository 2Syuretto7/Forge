import math
import sys

EPS = sys.float_info.epsilon

# provided
X = ("x",)


# provided
def c(v):
    return ("c", float(v))


# provided
FUNCTIONS = [
    (("^", X, 2), 1.5),
    (("^", X, 5), -0.7),
    (("sin", X), 0.4),
    (("cos", ("*", c(3), X)), 1.1),
    (("exp", ("*", c(-2), X)), 0.3),
    (("log", X), 2.5),
    (("log", ("+", X, c(1))), 0.01),
    (("tanh", X), 0.8),
    (("/", c(1), X), 0.6),
    (("/", ("sin", X), X), 1.3),
    (("*", X, ("exp", X)), -1.2),
    (("*", ("^", X, 3), ("sin", X)), 2.0),
    (("exp", ("sin", X)), 0.9),
    (("sin", ("exp", X)), 0.5),
    (("log", ("^", X, 2)), 3.0),
    (("tanh", ("*", c(5), X)), 0.1),
    (("/", ("exp", X), ("+", c(1), ("exp", X))), -0.4),
    (("^", ("+", c(1), ("^", X, 2)), -0.5), 0.7),
    (("-", ("*", c(2), X), ("log", X)), 4.0),
    (("*", ("cos", X), ("cos", X)), 0.25),
    (("exp", ("^", X, 2)), 1.4),
    (("log", ("+", c(1), ("exp", X))), -2.0),
    (("/", X, ("+", c(1), ("^", X, 2))), 1.7),
    (("sin", ("sin", ("sin", X))), 1.0),
    (("^", ("sin", X), 3), 0.6),
    (("*", ("exp", ("*", c(-1), X)), ("sin", ("*", c(10), X))), 0.2),
    (("log", ("cos", X)), 0.3),
    (("tanh", ("tanh", X)), -0.6),
    (("/", c(1), ("+", c(1), ("exp", ("*", c(-1), X)))), 0.0),
    (("^", X, 0.5), 9.0),
]


def evaluate(e, x):
    """Value of the tree at x."""
    op = e[0]
    if op == "x":
        return x
    if op == "c":
        return e[1]
    if op == "^":
        return evaluate(e[1], x) ** e[2]
    if op in ("+", "-", "*", "/"):
        a, b = evaluate(e[1], x), evaluate(e[2], x)
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        return a * b if op == "*" else a / b
    return {"sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "tanh": math.tanh}[op](evaluate(e[1], x))


def derivative(e):
    """Tree of the derivative."""
    op = e[0]
    if op == "x":
        return ("c", 1.0)
    if op == "c":
        return ("c", 0.0)
    if op in ("+", "-"):
        return (op, derivative(e[1]), derivative(e[2]))
    if op == "*":
        a, b = e[1], e[2]
        return ("+", ("*", derivative(a), b), ("*", a, derivative(b)))
    if op == "/":
        a, b = e[1], e[2]
        return ("/", ("-", ("*", derivative(a), b), ("*", a, derivative(b))), ("^", b, 2))
    if op == "^":
        a, k = e[1], e[2]
        return ("*", ("*", ("c", float(k)), ("^", a, k - 1)), derivative(a))
    a = e[1]
    outer = {
        "sin": ("cos", a),
        "cos": ("*", ("c", -1.0), ("sin", a)),
        "exp": ("exp", a),
        "log": ("/", ("c", 1.0), a),
        "tanh": ("-", ("c", 1.0), ("^", ("tanh", a), 2)),
    }[op]
    return ("*", outer, derivative(a))


def budget(e, x, h):
    """Expected error of the central difference at step h."""
    f = abs(evaluate(e, x))
    d1 = abs(evaluate(derivative(e), x))
    d3 = abs(evaluate(derivative(derivative(derivative(e))), x))
    return h * h / 6 * d3 + EPS * f / h + EPS * d1


def best_h(e, x):
    """Step minimizing truncation plus rounding."""
    f = abs(evaluate(e, x))
    d3 = abs(evaluate(derivative(derivative(derivative(e))), x))
    fallback = EPS ** (1 / 3) * max(1.0, abs(x))
    if f == 0 or d3 == 0:
        return fallback
    return max((3 * EPS * f / d3) ** (1 / 3), 1e-3 * fallback)


def verify(e, x, d=None):
    """(ok, error, allowed) comparing a derivative tree with a central difference."""
    d = derivative(e) if d is None else d
    h = best_h(e, x)
    central = (evaluate(e, x + h) - evaluate(e, x - h)) / (2 * h)
    err = abs(evaluate(d, x) - central)
    allowed = 10 * budget(e, x, h)
    return err <= allowed, err, allowed

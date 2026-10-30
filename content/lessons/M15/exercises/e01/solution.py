import math


def evaluate(e, x):
    """Value of the expression tree at x."""
    op = e[0]
    if op == "x":
        return x
    if op == "c":
        return e[1]
    if op == "+":
        return evaluate(e[1], x) + evaluate(e[2], x)
    if op == "*":
        return evaluate(e[1], x) * evaluate(e[2], x)
    if op == "^":
        return evaluate(e[1], x) ** e[2]
    return {"sin": math.sin, "cos": math.cos, "exp": math.exp}[op](evaluate(e[1], x))


def derivative(e):
    """Tree of the derivative."""
    op = e[0]
    if op == "x":
        return ("c", 1.0)
    if op == "c":
        return ("c", 0.0)
    if op == "+":
        return ("+", derivative(e[1]), derivative(e[2]))
    if op == "*":
        a, b = e[1], e[2]
        return ("+", ("*", derivative(a), b), ("*", a, derivative(b)))
    if op == "^":
        a, k = e[1], e[2]
        return ("*", ("*", ("c", float(k)), ("^", a, k - 1)), derivative(a))
    a = e[1]
    outer = {"sin": ("cos", a), "cos": ("*", ("c", -1.0), ("sin", a)), "exp": ("exp", a)}[op]
    return ("*", outer, derivative(a))


def size(e):
    """Number of nodes."""
    return 1 + sum(size(c) for c in e[1:] if isinstance(c, tuple))

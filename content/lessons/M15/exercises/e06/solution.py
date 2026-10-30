import math


def exp_quotient(h):
    """(e^h - 1) / h."""
    return (math.exp(h) - 1) / h


def sin_quotient(h):
    """sin(h) / h."""
    return math.sin(h) / h


def log_slope(x, h):
    """(ln(x + h) - ln x) / h."""
    return (math.log(x + h) - math.log(x)) / h


def order_of_error(q, limit, h):
    """|q(h) - L| / |q(h/2) - L|."""
    return abs(q(h) - limit) / abs(q(h / 2) - limit)

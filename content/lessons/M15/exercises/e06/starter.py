import math


def exp_quotient(h):
    """(e^h - 1) / h."""
    raise NotImplementedError


def sin_quotient(h):
    """sin(h) / h."""
    raise NotImplementedError


def log_slope(x, h):
    """(ln(x + h) - ln x) / h."""
    raise NotImplementedError


def order_of_error(q, limit, h):
    """|q(h) - L| / |q(h/2) - L|."""
    raise NotImplementedError

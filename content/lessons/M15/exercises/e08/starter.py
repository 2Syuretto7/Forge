def tangent(f, df, a):
    """The tangent line at a, as a function."""
    raise NotImplementedError


def linear_error(f, df, a, h):
    """|f(a + h) - f(a) - f'(a) h|."""
    raise NotImplementedError


def error_order(f, df, a, h):
    """linear_error(h) / linear_error(h / 2)."""
    raise NotImplementedError

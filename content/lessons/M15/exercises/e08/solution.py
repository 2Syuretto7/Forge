def tangent(f, df, a):
    """The tangent line at a, as a function."""
    fa, s = f(a), df(a)
    return lambda x: fa + s * (x - a)


def linear_error(f, df, a, h):
    """|f(a + h) - f(a) - f'(a) h|."""
    return abs(f(a + h) - f(a) - df(a) * h)


def error_order(f, df, a, h):
    """linear_error(h) / linear_error(h / 2)."""
    return linear_error(f, df, a, h) / linear_error(f, df, a, h / 2)

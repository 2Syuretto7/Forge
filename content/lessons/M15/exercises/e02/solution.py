def forward_diff(f, x, h):
    """Forward difference."""
    return (f(x + h) - f(x)) / h


def central_diff(f, x, h):
    """Central difference."""
    return (f(x + h) - f(x - h)) / (2 * h)


def error_ratio(f, df, x, h, method):
    """|error at h| / |error at h/2|."""
    d = forward_diff if method == "forward" else central_diff
    return abs(d(f, x, h) - df(x)) / abs(d(f, x, h / 2) - df(x))

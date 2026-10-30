def forward_diff(f, x, h):
    """Forward difference."""
    raise NotImplementedError


def central_diff(f, x, h):
    """Central difference."""
    raise NotImplementedError


def error_ratio(f, df, x, h, method):
    """|error at h| / |error at h/2|."""
    raise NotImplementedError

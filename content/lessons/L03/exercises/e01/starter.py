def forward_diff(f, x, h):
    raise NotImplementedError


def central_diff(f, x, h):
    raise NotImplementedError


def error_ratio(f, df, x, h, method):
    """|error at h| / |error at h/2| for method in {"forward", "central"}."""
    raise NotImplementedError

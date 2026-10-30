def pipeline(steps):
    """Apply steps left to right."""
    raise NotImplementedError


def standardize(xs):
    """(x - mean) / std with the population standard deviation."""
    raise NotImplementedError


def clip(xs, lo, hi):
    """Each value limited to [lo, hi]."""
    raise NotImplementedError


def order_matters(xs, lo, hi):
    """Whether clip-then-standardize differs from standardize-then-clip."""
    raise NotImplementedError

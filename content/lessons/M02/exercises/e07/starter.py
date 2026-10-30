def solve_inequality(a, b, c):
    """Solutions of a x + b < c: ("<", bound), (">", bound), "all" or None."""
    raise NotImplementedError


def abs_interval(center, radius):
    """(lo, hi) for |x - center| < radius, or None when radius <= 0."""
    raise NotImplementedError


def satisfies(a, b, c, x):
    """Whether x satisfies a x + b < c."""
    raise NotImplementedError

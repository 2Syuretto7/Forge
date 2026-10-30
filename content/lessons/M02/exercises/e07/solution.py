def solve_inequality(a, b, c):
    """Solutions of a x + b < c: ("<", bound), (">", bound), "all" or None."""
    if a == 0:
        return "all" if b < c else None
    bound = (c - b) / a
    return ("<", bound) if a > 0 else (">", bound)


def abs_interval(center, radius):
    """(lo, hi) for |x - center| < radius, or None when radius <= 0."""
    if radius <= 0:
        return None
    return center - radius, center + radius


def satisfies(a, b, c, x):
    """Whether x satisfies a x + b < c."""
    return a * x + b < c

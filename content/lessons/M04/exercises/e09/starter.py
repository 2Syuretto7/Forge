def max_error(f, g, a, b, m=2001):
    """Largest |f - g| over m equally spaced points of [a, b]."""
    raise NotImplementedError


def pl_interp(f, a, b, n):
    """Piecewise-linear interpolant of f on n equal pieces of [a, b]."""
    raise NotImplementedError


def pieces_needed(f, a, b, tol):
    """Smallest n with the n-piece interpolant within tol of f."""
    raise NotImplementedError

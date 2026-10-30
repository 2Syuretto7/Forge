def inverse(f, y, lo, hi, steps=60):
    """x in [lo, hi] with f(x) == y for increasing f, by bisection."""
    raise NotImplementedError


def make_inverse(f, lo, hi):
    """The machine y -> inverse(f, y, lo, hi)."""
    raise NotImplementedError

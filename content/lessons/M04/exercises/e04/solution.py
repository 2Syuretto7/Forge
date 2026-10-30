def inverse(f, y, lo, hi, steps=60):
    """x in [lo, hi] with f(x) == y for increasing f, by bisection."""
    if not f(lo) <= y <= f(hi):
        raise ValueError("y is not bracketed by f(lo) and f(hi)")
    for _ in range(steps):
        mid = (lo + hi) / 2
        if f(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def make_inverse(f, lo, hi):
    """The machine y -> inverse(f, y, lo, hi)."""
    return lambda y: inverse(f, y, lo, hi)

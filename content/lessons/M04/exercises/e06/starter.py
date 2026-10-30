def polynomial(coeffs):
    """x -> c0 + c1 x + ... + cn x^n, by Horner's rule."""
    raise NotImplementedError


def rational(p, q):
    """x -> P(x) / Q(x); ValueError where Q(x) == 0."""
    raise NotImplementedError


def piecewise(pieces):
    """Apply the f of the first (lo, hi, f) with lo <= x < hi; ValueError if none."""
    raise NotImplementedError

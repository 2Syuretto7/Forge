def polynomial(coeffs):
    """x -> c0 + c1 x + ... + cn x^n, by Horner's rule."""
    def machine(x):
        acc = 0
        for c in reversed(coeffs):
            acc = acc * x + c
        return acc
    return machine


def rational(p, q):
    """x -> P(x) / Q(x); ValueError where Q(x) == 0."""
    P, Q = polynomial(p), polynomial(q)

    def machine(x):
        d = Q(x)
        if d == 0:
            raise ValueError(f"the denominator is zero at {x}")
        return P(x) / d
    return machine


def piecewise(pieces):
    """Apply the f of the first (lo, hi, f) with lo <= x < hi; ValueError if none."""
    def machine(x):
        for lo, hi, f in pieces:
            if lo <= x < hi:
                return f(x)
        raise ValueError(f"{x} is in no piece")
    return machine

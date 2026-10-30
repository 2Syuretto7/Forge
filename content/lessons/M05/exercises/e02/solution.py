from fractions import Fraction


def partial_sums(term, n):
    """[S_1, ..., S_n] with S_k = term(1) + ... + term(k), exactly."""
    s = Fraction(0)
    out = []
    for k in range(1, n + 1):
        s += term(k)
        out.append(s)
    return out


def geometric_sum(r, n):
    """1 + r + ... + r^(n-1) by adding the terms."""
    return sum((r ** k for k in range(n)), Fraction(0))


def geometric_closed(r, n):
    """(r^n - 1) / (r - 1), or n when r == 1."""
    if r == 1:
        return Fraction(n)
    return (r ** n - 1) / (r - 1)

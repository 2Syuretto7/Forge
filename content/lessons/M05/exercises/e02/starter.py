from fractions import Fraction


def partial_sums(term, n):
    """[S_1, ..., S_n] with S_k = term(1) + ... + term(k), exactly."""
    raise NotImplementedError


def geometric_sum(r, n):
    """1 + r + ... + r^(n-1) by adding the terms."""
    raise NotImplementedError


def geometric_closed(r, n):
    """(r^n - 1) / (r - 1), or n when r == 1."""
    raise NotImplementedError

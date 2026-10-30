from fractions import Fraction


def _trim(p):
    raise NotImplementedError


def peval(p, n):
    """Value of the polynomial at n (Horner's rule)."""
    raise NotImplementedError


def padd(p, q):
    """p + q."""
    raise NotImplementedError


def pscale(p, c):
    """c * p."""
    raise NotImplementedError


def pmul(p, q):
    """p * q."""
    raise NotImplementedError


def pshift(p):
    """The polynomial p(n + 1)."""
    raise NotImplementedError


def pequal(p, q):
    """Equal coefficient lists after trimming trailing zeros."""
    raise NotImplementedError


def induction_check(f, F):
    """(base_ok, step_ok) for the claim sum_{k=1}^n f(k) == F(n)."""
    raise NotImplementedError

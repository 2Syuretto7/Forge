import math


def fermi(factors):
    """Return (lo, hi) of the product of [lo, hi] factors, each with op '*' or '/'."""
    raise NotImplementedError


def central(factors):
    """Geometric midpoint of the worksheet's interval."""
    raise NotImplementedError


def worst_factor(factors):
    """sqrt(hi / lo) of the worksheet's interval."""
    raise NotImplementedError


def typical_factor(factors):
    """10 ** sqrt(sum of squared log10 half-widths)."""
    raise NotImplementedError

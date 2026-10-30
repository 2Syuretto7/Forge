import math


def fermi(factors):
    """Return (lo, hi) of the product of [lo, hi] factors, each with op '*' or '/'."""
    lo, hi = 1.0, 1.0
    for f_lo, f_hi, op in factors:
        if op == "*":
            lo, hi = lo * f_lo, hi * f_hi
        else:
            lo, hi = lo / f_hi, hi / f_lo
    return lo, hi


def central(factors):
    """Geometric midpoint of the worksheet's interval."""
    lo, hi = fermi(factors)
    return math.sqrt(lo * hi)


def worst_factor(factors):
    """sqrt(hi / lo) of the worksheet's interval."""
    lo, hi = fermi(factors)
    return math.sqrt(hi / lo)


def typical_factor(factors):
    """10 ** sqrt(sum of squared log10 half-widths)."""
    h = [math.log10(math.sqrt(f_hi / f_lo)) for f_lo, f_hi, _ in factors]
    return 10 ** math.sqrt(sum(x * x for x in h))

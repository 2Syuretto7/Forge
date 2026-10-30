import math


def remainder(r, n):
    """1/(1 - r) minus the sum of the first n terms."""
    raise NotImplementedError


def terms_needed(r, eps):
    """Smallest n with remainder(r, n) < eps."""
    raise NotImplementedError


def work_ratio(r1, r2, eps):
    """terms_needed(r2) / terms_needed(r1)."""
    raise NotImplementedError

import math
import random


def p_shared(m, days=365):
    """Exact chance that two of m people share a birthday."""
    raise NotImplementedError


def p_shared_approx(m, days=365):
    """1 - exp(-m (m - 1) / (2 days))."""
    raise NotImplementedError


def smallest_room(target, days=365):
    """Smallest m with p_shared(m) >= target."""
    raise NotImplementedError


def simulate_room(m, n, seed=0):
    """Fraction of n random rooms of m people with a shared birthday."""
    raise NotImplementedError

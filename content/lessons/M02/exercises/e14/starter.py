import random


def squaring_keeps_order(a, b):
    """For a < b: whether a^2 < b^2."""
    raise NotImplementedError


def find_counterexample(trials=1000, seed=0):
    """First random pair a < b with a^2 >= b^2, or None."""
    raise NotImplementedError


def safe_to_square(a, b):
    """True when both are non-negative, so a < b implies a^2 < b^2."""
    raise NotImplementedError

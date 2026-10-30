import math
import random


def simulate(trial, n, seed=0):
    """Fraction of n runs of trial(rng) that return True."""
    raise NotImplementedError


def standard_error(p, n):
    """sqrt(p (1 - p) / n)."""
    raise NotImplementedError


def z_score(estimate, p, n):
    """Gap in standard errors."""
    raise NotImplementedError


def roll_two_sum_seven(rng):
    """Two dice sum to 7."""
    raise NotImplementedError

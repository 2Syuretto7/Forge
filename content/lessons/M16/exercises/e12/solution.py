import math


def efficiency(p, w):
    """p^(1/w)."""
    return p ** (1 / w)


def evaluations_for_digits(p, w, start_digits, digits):
    """Evaluations to reach the digits."""
    d, steps = float(start_digits), 0
    while d < digits:
        d *= p
        steps += 1
    return steps * w


def bisect_evaluations(digits):
    """Evaluations for bisection."""
    return math.ceil(digits / math.log10(2))

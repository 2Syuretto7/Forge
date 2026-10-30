import math


def round_sig(x, n):
    """Round x to n significant figures."""
    if x == 0:
        return 0
    return round(x, n - 1 - math.floor(math.log10(abs(x))))


def relative_error(estimate, truth):
    """Return |estimate - truth| / |truth|."""
    return abs(estimate - truth) / abs(truth)


def factor_off(estimate, truth):
    """Return max(estimate/truth, truth/estimate) for positive numbers; ValueError otherwise."""
    if estimate <= 0 or truth <= 0:
        raise ValueError("factor_off needs positive numbers")
    return max(estimate / truth, truth / estimate)

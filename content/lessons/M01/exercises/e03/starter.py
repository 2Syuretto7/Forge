import math


def round_sig(x, n):
    """Round x to n significant figures."""
    raise NotImplementedError


def relative_error(estimate, truth):
    """Return |estimate - truth| / |truth|."""
    raise NotImplementedError


def factor_off(estimate, truth):
    """Return max(estimate/truth, truth/estimate) for positive numbers; ValueError otherwise."""
    raise NotImplementedError

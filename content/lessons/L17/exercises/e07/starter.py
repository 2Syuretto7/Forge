import numpy as np


def round_down_up(x, step):
    """The two grid points around x on a grid of spacing `step`."""
    raise NotImplementedError


def stochastic_round(x, step, rng):
    """Round x to lo or hi = lo + step, choosing hi with probability (x - lo) / step."""
    raise NotImplementedError


def accumulate(w0, update, n, step, mode, rng=None):
    """Apply w <- round(w + update) n times on a grid of spacing `step`, with round-to-nearest or
    stochastic rounding."""
    raise NotImplementedError

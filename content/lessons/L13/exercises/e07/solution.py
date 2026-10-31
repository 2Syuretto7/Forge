import numpy as np


def round_down_up(x, step):
    """The two grid points around x on a grid of spacing `step`."""
    lo = np.floor(x / step) * step
    return lo, lo + step


def stochastic_round(x, step, rng):
    """Round x to lo or hi = lo + step, choosing hi with probability (x - lo) / step."""
    lo, hi = round_down_up(x, step)
    return np.where(rng.random(np.shape(x)) < (x - lo) / step, hi, lo)


def accumulate(w0, update, n, step, mode, rng=None):
    """Apply w <- round(w + update) n times on a grid of spacing `step`, with round-to-nearest or
    stochastic rounding."""
    w = w0
    for _ in range(n):
        v = w + update
        w = float(np.round(v / step) * step) if mode == "nearest" else float(stochastic_round(v, step, rng))
    return w

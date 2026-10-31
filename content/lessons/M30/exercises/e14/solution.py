import numpy as np


def naive_gibbs(r, tau):
    """Gibbs distribution as written."""
    with np.errstate(all="ignore"):
        e = np.exp(np.asarray(r, dtype=float) / tau)
        return e / e.sum()


def stable_gibbs(r, tau):
    """Gibbs distribution with the maximum subtracted."""
    r = np.asarray(r, dtype=float)
    e = np.exp((r - r.max()) / tau)
    return e / e.sum()


def limit_low(r):
    """Uniform over the maximizers."""
    r = np.asarray(r, dtype=float)
    top = np.isclose(r, r.max())
    return top / top.sum()


def limit_high(r):
    """Uniform."""
    return np.full(len(r), 1 / len(r))

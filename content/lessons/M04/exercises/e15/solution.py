import numpy as np


def silent_failures(xs):
    """Indices where np.sqrt or np.log of xs is not finite."""
    with np.errstate(all="ignore"):
        a, b = np.sqrt(xs), np.log(xs)
    return np.flatnonzero(~np.isfinite(a) | ~np.isfinite(b))


def poisoned_mean(xs):
    """Naive mean of np.log(xs)."""
    with np.errstate(all="ignore"):
        return float(np.mean(np.log(xs)))


def strict_log(xs):
    """np.log(xs) when every entry is positive; ValueError otherwise."""
    bad = np.flatnonzero(xs <= 0)
    if bad.size:
        raise ValueError(f"{bad.size} entries outside the domain of log, first at index {bad[0]}")
    return np.log(xs)

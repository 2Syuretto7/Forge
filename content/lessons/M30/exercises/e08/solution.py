import numpy as np


def gibbs(r, tau):
    """Softmax of r / tau."""
    r = np.asarray(r, dtype=float)
    e = np.exp((r - r.max()) / tau)
    return e / e.sum()


def objective(p, r, tau):
    """Expected reward plus tau times entropy."""
    p, r = np.asarray(p, dtype=float), np.asarray(r, dtype=float)
    q = p[p > 0]
    return float(p @ r - tau * np.sum(q * np.log(q)))


def value(r, tau):
    """tau log sum exp(r / tau)."""
    r = np.asarray(r, dtype=float)
    m = r.max()
    return float(m + tau * np.log(np.sum(np.exp((r - m) / tau))))

import numpy as np


def kl_optimum(pi, r, beta):
    """The maximizer of expected reward minus beta KL(p || pi)."""
    z = np.log(np.asarray(pi, dtype=float)) + np.asarray(r, dtype=float) / beta
    e = np.exp(z - z.max())
    return e / e.sum()


def kl_objective(p, pi, r, beta):
    """Expected reward minus beta KL(p || pi)."""
    p, pi, r = (np.asarray(v, dtype=float) for v in (p, pi, r))
    m = p > 0
    return float(p @ r - beta * np.sum(p[m] * np.log(p[m] / pi[m])))


def implied_reward(p, pi, beta):
    """beta log(p / pi)."""
    return beta * np.log(np.asarray(p, dtype=float) / np.asarray(pi, dtype=float))

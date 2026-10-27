import numpy as np


def total_variation(p, q):
    return float(0.5 * np.sum(np.abs(np.asarray(p) - np.asarray(q))))


def _kl(p, q):
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = p > 0
    if np.any(q[m] == 0):
        return float("inf")
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


def pinsker_bound(p, q):
    return float(np.sqrt(0.5 * _kl(p, q)))


def worst_event(p, q):
    return np.asarray(p) > np.asarray(q)

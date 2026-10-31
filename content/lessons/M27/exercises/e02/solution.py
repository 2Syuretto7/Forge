import numpy as np


def cross_entropy(p, q):
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = p > 0
    if np.any(q[m] == 0):
        return float("inf")
    return float(-np.sum(p[m] * np.log(q[m])))


def kl(p, q):
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = p > 0
    if np.any(q[m] == 0):
        return float("inf")
    return float(np.sum(p[m] * np.log(p[m] / q[m])))

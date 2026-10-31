import math
import numpy as np


def kalman_1d(z, q, r, m0, p0):
    """Filtered means and variances of a random walk observed with noise."""
    m, p = m0, p0
    means, variances = [], []
    for zt in z:
        p = p + q
        K = p / (p + r)
        m = m + K * (zt - m)
        p = (1 - K) * p
        means.append(m)
        variances.append(p)
    return np.array(means), np.array(variances)


def steady_variance(q, r):
    """Settled variance after the update."""
    return (-q + math.sqrt(q * q + 4 * q * r)) / 2

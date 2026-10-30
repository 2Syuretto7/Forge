import math
import numpy as np


def ks_distance(samples, cdf):
    """Kolmogorov-Smirnov distance between the samples and a continuous CDF."""
    x = np.sort(np.asarray(samples, dtype=float))
    n = len(x)
    F = cdf(x)
    i = np.arange(1, n + 1)
    return float(max(np.max(i / n - F), np.max(F - (i - 1) / n)))


def discrete_distance(samples, cdf_values):
    """Largest CDF gap at the integers 0..K-1."""
    cdf_values = np.asarray(cdf_values, dtype=float)
    K = len(cdf_values)
    counts = np.bincount(np.asarray(samples), minlength=K)[:K]
    emp = np.cumsum(counts) / len(samples)
    return float(np.max(np.abs(emp - cdf_values)))


def dkw_threshold(n, alpha):
    """Distance a correct sampler exceeds with probability at most alpha."""
    return math.sqrt(math.log(2 / alpha) / (2 * n))

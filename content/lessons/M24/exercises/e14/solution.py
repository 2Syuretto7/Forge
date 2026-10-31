import math
import numpy as np


def pareto(alpha, size, rng):
    """Pareto(alpha) samples with x_m = 1."""
    return (1 - rng.random(size)) ** (-1 / alpha)


def coverage(samples, true_mean):
    """Fraction of rows whose CLT interval contains true_mean."""
    X = np.asarray(samples, dtype=float)
    m = X.mean(axis=1)
    h = 1.96 * X.std(axis=1, ddof=1) / math.sqrt(X.shape[1])
    return float(np.mean(np.abs(m - true_mean) <= h))

import math
import numpy as np


def normal_interval(values, z=1.96):
    """CLT interval for the mean."""
    v = np.asarray(values, dtype=float)
    m = v.mean()
    h = z * v.std(ddof=1) / math.sqrt(len(v))
    return float(m - h), float(m + h)


def coverage(draw, true_mean, n, runs, rng):
    """Fraction of runs whose interval contains the true mean."""
    X = np.asarray(draw(rng, (runs, n)), dtype=float)
    m = X.mean(axis=1)
    h = 1.96 * X.std(axis=1, ddof=1) / math.sqrt(n)
    return float(np.mean(np.abs(m - true_mean) <= h))


def n_for_halfwidth(sigma, h, z=1.96):
    """Samples needed for a halfwidth of h."""
    return math.ceil(round((z * sigma / h) ** 2, 9))

import math
import numpy as np


def coverage(intervals, truth):
    """Fraction of intervals that contain truth."""
    iv = np.asarray(intervals, dtype=float)
    return float(np.mean((iv[:, 0] <= truth) & (truth <= iv[:, 1])))


def hoeffding_intervals(accs, n, delta=0.05):
    """Hoeffding intervals around each accuracy."""
    a = np.asarray(accs, dtype=float)
    h = math.sqrt(math.log(2 / delta) / (2 * n))
    return np.column_stack([a - h, a + h])


def clt_intervals(accs, n, z=1.96):
    """Normal-approximation intervals around each accuracy."""
    a = np.asarray(accs, dtype=float)
    h = z * np.sqrt(a * (1 - a) / n)
    return np.column_stack([a - h, a + h])


def simulate(p, n, sets, rng):
    """Measured accuracies of independent test sets."""
    return rng.binomial(n, p, size=sets) / n

import numpy as np


def one_pass_var(x):
    """Mean of squares minus square of the mean, in the array's dtype."""
    x = np.asarray(x)
    return float(np.mean(x * x) - np.mean(x) ** 2)


def two_pass_var(x):
    """Mean squared deviation from the mean, computed in two passes."""
    x = np.asarray(x)
    m = np.mean(x)
    return float(np.mean((x - m) ** 2))


def welford_var(x):
    """Welford's streaming variance."""
    m, M = 0.0, 0.0
    for k, v in enumerate(np.asarray(x, dtype=float).tolist(), start=1):
        d = v - m
        m += d / k
        M += d * (v - m)
    return M / len(x)

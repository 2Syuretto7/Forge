import numpy as np


def iqr(v):
    """Interquartile range of a 1-D array."""
    q1, q3 = np.quantile(np.asarray(v, dtype=float), [0.25, 0.75])
    return float(q3 - q1)


def spread_of_means(samples):
    """IQR of the row means of samples (trials, n)."""
    return iqr(np.asarray(samples, dtype=float).mean(axis=1))


def spread_of_medians(samples):
    """IQR of the row medians of samples (trials, n)."""
    return iqr(np.median(np.asarray(samples, dtype=float), axis=1))

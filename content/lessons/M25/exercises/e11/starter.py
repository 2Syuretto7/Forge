import numpy as np


def bootstrap_means(x, B, seed=0):
    """Return (B,) means of resamples of x drawn with replacement."""
    raise NotImplementedError


def percentile_ci(stats, level=0.95):
    """Equal-tailed percentile interval (lo, hi)."""
    raise NotImplementedError


def coverage(true_mean, datasets, B=500, level=0.95, seed=0):
    """Fraction of rows of datasets (R, n) whose bootstrap interval contains true_mean."""
    raise NotImplementedError

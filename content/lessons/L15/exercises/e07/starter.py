import numpy as np


def mean_with_ci(values, n_boot=2000, seed=0, level=0.95):
    """The mean of per-example losses and a percentile bootstrap interval for it."""
    raise NotImplementedError


def paired_difference(a, b, n_boot=2000, seed=0, level=0.95):
    """Two checkpoints scored on the same examples: the mean of a - b and a bootstrap interval that
    resamples examples (keeping each pair together)."""
    raise NotImplementedError

import numpy as np


def paired_bootstrap(a, b, n_boot=2000, seed=0, level=0.95):
    """Two models' per-item correctness on the same items: the mean difference a - b and a
    bootstrap interval that resamples items (keeping each pair). Return (diff, low, high)."""
    raise NotImplementedError

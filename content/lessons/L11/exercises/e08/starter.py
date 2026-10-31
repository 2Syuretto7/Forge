import numpy as np


def bootstrap_exponent(x, y, n_boot=1000, seed=0, level=0.9):
    """Resample the runs with replacement n_boot times, refit y = k x^-a by a log-log line each
    time (skip resamples with fewer than two distinct x), and return the central `level` percentile
    interval of a as (low, high)."""
    raise NotImplementedError

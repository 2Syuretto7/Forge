import numpy as np


def bootstrap_exponent(x, y, n_boot=1000, seed=0, level=0.9):
    """Resample the runs with replacement n_boot times, refit y = k x^-a by a log-log line each
    time (skip resamples with fewer than two distinct x), and return the central `level` percentile
    interval of a as (low, high)."""
    rng = np.random.default_rng(seed)
    lx, ly = np.log(x), np.log(y)
    n = len(x)
    a = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if np.unique(idx).size < 2:
            continue
        a.append(-np.polyfit(lx[idx], ly[idx], 1)[0])
    low, high = np.quantile(a, [(1 - level) / 2, (1 + level) / 2])
    return low, high

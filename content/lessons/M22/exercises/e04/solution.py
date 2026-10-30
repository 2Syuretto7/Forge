import numpy as np


def expected_fixed_points(n):
    """Expected number of fixed points of a uniform random permutation of n items."""
    return n * (1.0 / n)


def simulate_fixed_points(n, trials, seed):
    """Average number of fixed points over random shuffles."""
    rng = np.random.default_rng(seed)
    perms = np.argsort(rng.random((trials, n)), axis=1)
    return float(np.mean(np.sum(perms == np.arange(n), axis=1)))


def expected_empty_bins(balls, bins):
    """Expected number of empty bins."""
    return bins * (1 - 1 / bins) ** balls


def expected_distinct_birthdays(n, days=365):
    """Expected number of distinct birthdays among n people."""
    return days - expected_empty_bins(n, days)

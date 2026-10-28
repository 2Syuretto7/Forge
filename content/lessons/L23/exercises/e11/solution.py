import numpy as np


def compare_models(acc_a, acc_b, n_items, seed=0, n_boot=2000):
    """Simulate two models with true accuracies acc_a and acc_b answering the same n_items
    (independently per item, with np.random.default_rng(seed)), and return the paired bootstrap
    interval (low, high) of the accuracy difference a - b."""
    rng = np.random.default_rng(seed)
    a = (rng.random(n_items) < acc_a).astype(float)
    b = (rng.random(n_items) < acc_b).astype(float)
    d = a - b
    means = d[rng.integers(0, n_items, (n_boot, n_items))].mean(axis=1)
    lo, hi = np.quantile(means, [0.025, 0.975])
    return float(lo), float(hi)

import numpy as np


def compare_models(acc_a, acc_b, n_items, seed=0, n_boot=2000):
    """Simulate two models with true accuracies acc_a and acc_b answering the same n_items
    (independently per item, with np.random.default_rng(seed)), and return the paired bootstrap
    interval (low, high) of the accuracy difference a - b."""
    raise NotImplementedError

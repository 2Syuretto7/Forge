import math
import numpy as np


# provided
def make_eval(seed=0):
    return (np.random.default_rng(seed).random(2000) < 0.87).astype(float)


def hoeffding_interval(correct, delta=0.05):
    """(accuracy, low, high) from Hoeffding's inequality."""
    raise NotImplementedError


def bootstrap_interval(correct, B=4000, seed=0, level=0.95):
    """(accuracy, low, high) from the percentile bootstrap."""
    raise NotImplementedError


def union_epsilon(n, k, delta=0.05):
    """Half-width that holds for k models at once."""
    raise NotImplementedError


def reuse_experiment(k=1000, n=1000, seed=0):
    """Selecting the best of k random models on one test set, then checking it on another."""
    raise NotImplementedError


# your answer
REPORT = """
"""

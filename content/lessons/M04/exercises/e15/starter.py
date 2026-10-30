import numpy as np


def silent_failures(xs):
    """Indices where np.sqrt or np.log of xs is not finite."""
    raise NotImplementedError


def poisoned_mean(xs):
    """Naive mean of np.log(xs)."""
    raise NotImplementedError


def strict_log(xs):
    """np.log(xs) when every entry is positive; ValueError otherwise."""
    raise NotImplementedError

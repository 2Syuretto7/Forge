import numpy as np


def accuracy_ci(correct, n_boot=2000, seed=0, level=0.95):
    """Accuracy over items (an array of 0/1) with a percentile bootstrap interval that resamples
    items. Return (accuracy, low, high)."""
    raise NotImplementedError


def standard_error(p, n):
    """The standard error of an accuracy p measured on n independent items."""
    raise NotImplementedError

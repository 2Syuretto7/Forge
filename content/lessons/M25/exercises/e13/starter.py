import numpy as np


def bootstrap_by_index(values, B, rng):
    """Bootstrap means by resampling indices."""
    raise NotImplementedError


def bootstrap_by_counts(values, B, rng):
    """Bootstrap means from multinomial counts of the distinct values."""
    raise NotImplementedError


def paired_interval(correct_a, correct_b, B, rng, level=0.95):
    """Percentile interval for the mean of correct_b - correct_a."""
    raise NotImplementedError

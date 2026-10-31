import math
import numpy as np


def running_mean(x):
    """Averages of the first 1, 2, ..., n entries."""
    raise NotImplementedError


def fraction_far(samples, mu, eps):
    """Fraction of rows whose mean misses mu by more than eps."""
    raise NotImplementedError


def chebyshev_n(var, eps, delta):
    """Samples Chebyshev needs for P(|mean - mu| >= eps) <= delta."""
    raise NotImplementedError

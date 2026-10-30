import math
import numpy as np


def ks_distance(samples, cdf):
    """Kolmogorov-Smirnov distance between the samples and a continuous CDF."""
    raise NotImplementedError


def discrete_distance(samples, cdf_values):
    """Largest CDF gap at the integers 0..K-1."""
    raise NotImplementedError


def dkw_threshold(n, alpha):
    """Distance a correct sampler exceeds with probability at most alpha."""
    raise NotImplementedError

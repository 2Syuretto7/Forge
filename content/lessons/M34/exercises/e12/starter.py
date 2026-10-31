import numpy as np


def _density(x, gamma):
    raise NotImplementedError


def mp_cdf(x, gamma):
    """Marchenko-Pastur CDF by numerical integration."""
    raise NotImplementedError


def ks_distance(eigs, gamma):
    """Kolmogorov-Smirnov distance to the Marchenko-Pastur law."""
    raise NotImplementedError


def ks_for_sizes(sizes, gamma, rng):
    """KS distance of sample-covariance eigenvalues for each size."""
    raise NotImplementedError

import math

import numpy as np


def normalizer(Sigma):
    """(2 pi)^(n/2) sqrt(det Sigma)."""
    raise NotImplementedError


def gaussian_density(x, Sigma):
    """Multivariate normal density with mean 0."""
    raise NotImplementedError


def sample_gaussian(Sigma, n, seed=0):
    """Rows x = L z."""
    raise NotImplementedError

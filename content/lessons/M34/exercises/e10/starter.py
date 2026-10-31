import math
import numpy as np


def sample_pairs(n, m, rng):
    """m random pairs of distinct indices."""
    raise NotImplementedError


def pair_distortions(X, pairs, k, rng):
    """Relative change of squared distances under a Gaussian projection."""
    raise NotImplementedError


def distortion_table(X, ks, m, rng):
    """Standard deviation and 99th percentile of absolute distortion for each k."""
    raise NotImplementedError

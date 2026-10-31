import math
import numpy as np


def jl_matrix(d, k, rng):
    """Gaussian projection matrix with N(0, 1/k) entries."""
    raise NotImplementedError


def pairwise_sq_dists(X):
    """Squared distances between all rows."""
    raise NotImplementedError


def max_sq_distortion(X, Y):
    """Largest relative change of a squared pairwise distance."""
    raise NotImplementedError


def jl_dim(n, eps):
    """Target dimension of the Johnson-Lindenstrauss lemma."""
    raise NotImplementedError

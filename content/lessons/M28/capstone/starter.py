import math
import numpy as np


def quadratic(eigs, seed):
    """Symmetric matrix with the given eigenvalues and random eigenvectors."""
    raise NotImplementedError


def gd_iterations(A, x0, step, eps=1e-6, max_iter=200000):
    """Gradient-descent iterations to relative error eps."""
    raise NotImplementedError


def predicted_iterations(A, x0, step, eps=1e-6):
    """Iterations from the eigendecomposition alone."""
    raise NotImplementedError


def rate_bound(eigs, step, eps=1e-6):
    """Iterations guaranteed by the worst contraction factor."""
    raise NotImplementedError


def lab(d=40, seed=0):
    """Ten quadratics: predicted, actual and bound."""
    raise NotImplementedError

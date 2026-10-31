import numpy as np


def ellipse_axes(Sigma):
    """(eigenvalues decreasing, eigenvectors as columns)."""
    raise NotImplementedError


def mahalanobis(X, mu, Sigma):
    """Mahalanobis distance of each row of X."""
    raise NotImplementedError


def prob_inside(k):
    """P(r <= k) for a 2D Gaussian."""
    raise NotImplementedError


def ellipse_points(mu, Sigma, k, m=100):
    """Points on the contour r = k."""
    raise NotImplementedError

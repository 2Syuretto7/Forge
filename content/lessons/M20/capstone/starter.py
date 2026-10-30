import math

import numpy as np

# provided
SIGMA = np.array([[2.0, 0.9], [0.9, 1.0]])
L = np.linalg.cholesky(SIGMA)


def exp_map(u):
    """Exponential with rate 2."""
    raise NotImplementedError


def exp_inverse(y):
    """u from y."""
    raise NotImplementedError


def exp_density(y):
    """2 e^(-2y) on y >= 0."""
    raise NotImplementedError


def bm_map(u):
    """Box-Muller."""
    raise NotImplementedError


def bm_inverse(xy):
    """(u1, u2) from (x, y)."""
    raise NotImplementedError


def bm_density(xy):
    """Standard bivariate normal."""
    raise NotImplementedError


def disc_map(u):
    """Uniform on the unit disc."""
    raise NotImplementedError


def disc_inverse(xy):
    """(u1, u2) from a point of the disc."""
    raise NotImplementedError


def disc_density(xy):
    """1/pi inside the disc."""
    raise NotImplementedError


def cauchy_map(u):
    """Standard Cauchy."""
    raise NotImplementedError


def cauchy_inverse(y):
    """u from y."""
    raise NotImplementedError


def cauchy_density(y):
    """1 / (pi (1 + y^2))."""
    raise NotImplementedError


def corr_map(u):
    """L times a Box-Muller pair."""
    raise NotImplementedError


def corr_inverse(xy):
    """Undo L, then Box-Muller."""
    raise NotImplementedError


def corr_density(xy):
    """Bivariate normal with covariance SIGMA."""
    raise NotImplementedError


def _absdet(inverse, y, h=1e-6):
    raise NotImplementedError


def cov_check(inverse, density, points):
    """Worst relative gap between the density and |det J| of the inverse."""
    raise NotImplementedError


def hist_check_1d(samples, density, lo, hi, bins):
    """Worst relative deviation of a 1-D histogram."""
    raise NotImplementedError


def hist_check_2d(samples, density, box, bins):
    """Worst relative deviation of a 2-D histogram over well-filled bins inside the support."""
    raise NotImplementedError


def report(n=200_000, seed=0):
    """Both checks for every sampler."""
    raise NotImplementedError

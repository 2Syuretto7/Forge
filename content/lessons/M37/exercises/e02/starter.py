import math
import numpy as np


def ou_mean_var(x0, t, theta, mu, sigma):
    """Exact mean and variance of X_t given X_0 = x0."""
    raise NotImplementedError


def ou_exact_step(x, dt, theta, mu, sigma, rng):
    """One exact transition."""
    raise NotImplementedError


def ou_path(x0, n, dt, theta, mu, sigma, rng):
    """A path of n states by exact steps."""
    raise NotImplementedError


def stationary_var(theta, sigma):
    """Variance of the stationary distribution."""
    raise NotImplementedError

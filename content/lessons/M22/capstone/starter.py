import math
import numpy as np


def _inverse_cdf_table(pmf, size, rng):
    raise NotImplementedError


def bernoulli(p, size, rng):
    """Bernoulli(p) samples."""
    raise NotImplementedError


def binomial(n, p, size, rng):
    """Binomial(n, p) samples by the inverse CDF."""
    raise NotImplementedError


def geometric(p, size, rng):
    """Trials up to and including the first success."""
    raise NotImplementedError


def poisson(lam, size, rng):
    """Poisson(lam) samples by the inverse CDF."""
    raise NotImplementedError


def uniform(a, b, size, rng):
    """Uniform(a, b) samples."""
    raise NotImplementedError


def exponential(lam, size, rng):
    """Exponential(lam) samples by the inverse CDF."""
    raise NotImplementedError


def laplace(b, size, rng):
    """Laplace(0, b) samples by the inverse CDF."""
    raise NotImplementedError


def gaussian(mu, sigma, size, rng):
    """N(mu, sigma^2) samples by Box-Muller."""
    raise NotImplementedError


def leaky_second_moment(a):
    """E[f(Z)^2] for the leaky ReLU with slope a and a standard normal Z."""
    raise NotImplementedError


def init_std(fan_in, a):
    """Weight standard deviation that preserves the second moment."""
    raise NotImplementedError


def depth_check(depth, width, a, multiplier=1.0, seed=0):
    """Second moments after each of depth leaky-ReLU layers."""
    raise NotImplementedError

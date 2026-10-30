import math
import numpy as np

_erf = np.vectorize(math.erf)


def uniform_pdf(x, a, b):
    """Density of Uniform(a, b)."""
    raise NotImplementedError


def uniform_cdf(x, a, b):
    """CDF of Uniform(a, b)."""
    raise NotImplementedError


def exponential_pdf(x, lam):
    """Density of Exponential(lam)."""
    raise NotImplementedError


def exponential_cdf(x, lam):
    """CDF of Exponential(lam)."""
    raise NotImplementedError


def normal_pdf(x, mu, sigma):
    """Density of N(mu, sigma^2)."""
    raise NotImplementedError


def normal_cdf(x, mu, sigma):
    """CDF of N(mu, sigma^2)."""
    raise NotImplementedError

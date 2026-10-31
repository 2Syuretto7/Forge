import numpy as np


def mgf_bernoulli(t, p):
    """MGF of Bernoulli(p)."""
    raise NotImplementedError


def mgf_normal(t, mu, sigma):
    """MGF of N(mu, sigma^2)."""
    raise NotImplementedError


def mgf_exponential(t, lam):
    """MGF of Exponential(lam), for t < lam."""
    raise NotImplementedError


def moments_from_mgf(M, h=1e-4):
    """(E X, E X^2) from central differences of M at 0."""
    raise NotImplementedError


def mgf_of_sum(M, n):
    """MGF of the sum of n independent copies."""
    raise NotImplementedError

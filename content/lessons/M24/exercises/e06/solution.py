import numpy as np


def mgf_bernoulli(t, p):
    """MGF of Bernoulli(p)."""
    return 1 - p + p * np.exp(t)


def mgf_normal(t, mu, sigma):
    """MGF of N(mu, sigma^2)."""
    return np.exp(mu * t + 0.5 * sigma**2 * np.asarray(t, dtype=float) ** 2)


def mgf_exponential(t, lam):
    """MGF of Exponential(lam), for t < lam."""
    return lam / (lam - np.asarray(t, dtype=float))


def moments_from_mgf(M, h=1e-4):
    """(E X, E X^2) from central differences of M at 0."""
    return (M(h) - M(-h)) / (2 * h), (M(h) - 2 * M(0.0) + M(-h)) / (h * h)


def mgf_of_sum(M, n):
    """MGF of the sum of n independent copies."""
    return lambda t: M(t) ** n

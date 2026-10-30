import math
import numpy as np

_erf = np.vectorize(math.erf)


def uniform_pdf(x, a, b):
    """Density of Uniform(a, b)."""
    x = np.asarray(x, dtype=float)
    return np.where((x >= a) & (x <= b), 1.0 / (b - a), 0.0)


def uniform_cdf(x, a, b):
    """CDF of Uniform(a, b)."""
    return np.clip((np.asarray(x, dtype=float) - a) / (b - a), 0.0, 1.0)


def exponential_pdf(x, lam):
    """Density of Exponential(lam)."""
    x = np.asarray(x, dtype=float)
    return np.where(x >= 0, lam * np.exp(-lam * np.maximum(x, 0)), 0.0)


def exponential_cdf(x, lam):
    """CDF of Exponential(lam)."""
    x = np.asarray(x, dtype=float)
    return np.where(x >= 0, -np.expm1(-lam * np.maximum(x, 0)), 0.0)


def normal_pdf(x, mu, sigma):
    """Density of N(mu, sigma^2)."""
    z = (np.asarray(x, dtype=float) - mu) / sigma
    return np.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))


def normal_cdf(x, mu, sigma):
    """CDF of N(mu, sigma^2)."""
    z = (np.asarray(x, dtype=float) - mu) / (sigma * math.sqrt(2))
    return 0.5 * (1 + _erf(z))

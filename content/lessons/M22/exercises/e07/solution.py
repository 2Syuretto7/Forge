import numpy as np


def laplace_pdf(x, b):
    """Density of the Laplace distribution with scale b."""
    return np.exp(-np.abs(np.asarray(x, dtype=float)) / b) / (2 * b)


def laplace_quantile(u, b):
    """Inverse CDF of the Laplace distribution."""
    u = np.asarray(u, dtype=float)
    lo = b * np.log(2 * np.minimum(u, 0.5))
    hi = -b * np.log(2 * (1 - np.maximum(u, 0.5)))
    return np.where(u < 0.5, lo, hi)


def cauchy_pdf(x):
    """Density of the standard Cauchy distribution."""
    x = np.asarray(x, dtype=float)
    return 1 / (np.pi * (1 + x * x))


def cauchy_quantile(u):
    """Inverse CDF of the standard Cauchy distribution."""
    return np.tan(np.pi * (np.asarray(u, dtype=float) - 0.5))


def pareto_pdf(x, alpha, xm):
    """Density of the Pareto distribution."""
    x = np.asarray(x, dtype=float)
    return np.where(x >= xm, alpha * xm**alpha / np.maximum(x, xm) ** (alpha + 1), 0.0)


def pareto_quantile(u, alpha, xm):
    """Inverse CDF of the Pareto distribution."""
    return xm * (1 - np.asarray(u, dtype=float)) ** (-1 / alpha)

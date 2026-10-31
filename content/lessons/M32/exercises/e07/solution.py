import math
import numpy as np


def gibbs_bivariate(rho, n, rng):
    """Gibbs sampler for the standard bivariate normal with correlation rho."""
    z = rng.standard_normal((n, 2))
    c = math.sqrt(1 - rho * rho)
    out = np.empty((n, 2))
    x = y = 0.0
    for i in range(n):
        x = rho * y + c * z[i, 0]
        y = rho * x + c * z[i, 1]
        out[i] = (x, y)
    return out


def lag1(x):
    """Lag-one autocorrelation."""
    x = np.asarray(x, dtype=float) - np.mean(x)
    return float(np.dot(x[:-1], x[1:]) / np.dot(x, x))


def gibbs_gaussian(mu, cov, n, rng):
    """Systematic-scan Gibbs sampler for N(mu, cov)."""
    mu = np.asarray(mu, dtype=float)
    L = np.linalg.inv(np.asarray(cov, dtype=float))
    d = len(mu)
    x = mu.copy()
    z = rng.standard_normal((n, d))
    out = np.empty((n, d))
    for t in range(n):
        for i in range(d):
            m = mu[i] - (L[i] @ (x - mu) - L[i, i] * (x[i] - mu[i])) / L[i, i]
            x[i] = m + z[t, i] / math.sqrt(L[i, i])
        out[t] = x
    return out

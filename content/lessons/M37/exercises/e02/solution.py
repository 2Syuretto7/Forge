import math
import numpy as np


def ou_mean_var(x0, t, theta, mu, sigma):
    """Exact mean and variance of X_t given X_0 = x0."""
    e = math.exp(-theta * t)
    return mu + (x0 - mu) * e, sigma**2 / (2 * theta) * (1 - e * e)


def ou_exact_step(x, dt, theta, mu, sigma, rng):
    """One exact transition."""
    e = math.exp(-theta * dt)
    v = sigma**2 / (2 * theta) * (1 - e * e)
    x = np.asarray(x, dtype=float)
    return mu + (x - mu) * e + math.sqrt(v) * rng.standard_normal(x.shape)


def ou_path(x0, n, dt, theta, mu, sigma, rng):
    """A path of n states by exact steps."""
    e = math.exp(-theta * dt)
    sd = math.sqrt(sigma**2 / (2 * theta) * (1 - e * e))
    z = rng.standard_normal(n)
    out = np.empty(n)
    x = x0
    for i in range(n):
        x = mu + (x - mu) * e + sd * z[i]
        out[i] = x
    return out


def stationary_var(theta, sigma):
    """Variance of the stationary distribution."""
    return sigma**2 / (2 * theta)

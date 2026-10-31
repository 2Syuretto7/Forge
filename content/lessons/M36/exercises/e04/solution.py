import numpy as np


def reparam_samples(fprime, mu, sigma, n, rng):
    """Pathwise gradient estimates in (mu, sigma)."""
    eps = rng.standard_normal(n)
    d = fprime(mu + sigma * eps)
    return np.stack([d, d * eps], axis=1)


def score_samples(f, mu, sigma, n, rng):
    """Score-function gradient estimates in (mu, sigma)."""
    eps = rng.standard_normal(n)
    x = mu + sigma * eps
    fx = f(x)
    return np.stack([fx * (x - mu) / sigma**2, fx * ((x - mu) ** 2 / sigma**3 - 1 / sigma)], axis=1)


def exact_grad_square(mu, sigma):
    """Gradient of E x^2 = mu^2 + sigma^2."""
    return np.array([2 * mu, 2 * sigma])

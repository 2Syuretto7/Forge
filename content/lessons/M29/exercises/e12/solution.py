import numpy as np


def stationary_variance(eta, mu, sigma, B):
    """Variance of the stationary distribution of constant-step SGD on a quadratic."""
    return eta * sigma**2 / (B * mu * (2 - eta * mu))


def simulate(eta, mu, sigma, B, chains, steps, rng):
    """Final values of many independent SGD chains."""
    x = np.zeros(chains)
    for _ in range(steps):
        x = (1 - eta * mu) * x - eta * sigma * rng.standard_normal(chains) / np.sqrt(B)
    return x

import numpy as np


def stationary_variance(eta, mu, sigma, B):
    """Variance of the stationary distribution of constant-step SGD on a quadratic."""
    raise NotImplementedError


def simulate(eta, mu, sigma, B, chains, steps, rng):
    """Final values of many independent SGD chains."""
    raise NotImplementedError

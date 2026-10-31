import numpy as np


def reparam_samples(fprime, mu, sigma, n, rng):
    """Pathwise gradient estimates in (mu, sigma)."""
    raise NotImplementedError


def score_samples(f, mu, sigma, n, rng):
    """Score-function gradient estimates in (mu, sigma)."""
    raise NotImplementedError


def exact_grad_square(mu, sigma):
    """Gradient of E x^2 = mu^2 + sigma^2."""
    raise NotImplementedError

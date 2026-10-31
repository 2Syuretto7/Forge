import numpy as np


def rademacher_linear(X, B, draws, rng):
    """Monte Carlo estimate of the empirical Rademacher complexity."""
    raise NotImplementedError


def rademacher_bound(X, B):
    """B sqrt(sum |x_i|^2) / n."""
    raise NotImplementedError

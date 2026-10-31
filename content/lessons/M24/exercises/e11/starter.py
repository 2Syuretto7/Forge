import numpy as np


def _mean_se(v):
    raise NotImplementedError


def pathwise_grad(fprime, theta, n, rng):
    """Pathwise estimate of d/dtheta E[f(theta + z)]."""
    raise NotImplementedError


def score_grad(f, theta, n, rng):
    """Score-function estimate of d/dtheta E[f(x)], x ~ N(theta, 1)."""
    raise NotImplementedError

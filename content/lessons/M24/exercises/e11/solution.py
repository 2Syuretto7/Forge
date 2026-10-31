import numpy as np


def _mean_se(v):
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))


def pathwise_grad(fprime, theta, n, rng):
    """Pathwise estimate of d/dtheta E[f(theta + z)]."""
    z = rng.standard_normal(n)
    return _mean_se(fprime(theta + z))


def score_grad(f, theta, n, rng):
    """Score-function estimate of d/dtheta E[f(x)], x ~ N(theta, 1)."""
    z = rng.standard_normal(n)
    return _mean_se(f(theta + z) * z)

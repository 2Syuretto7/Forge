import numpy as np


def likelihood_product(ps):
    """Product of the probabilities in float64."""
    return float(np.prod(np.asarray(ps, dtype=np.float64)))


def log_likelihood_naive(ps):
    """log of the product (minus infinity once it underflows)."""
    with np.errstate(divide="ignore"):
        return float(np.log(likelihood_product(ps)))


def log_likelihood(ps):
    """Sum of the logs."""
    return float(np.sum(np.log(np.asarray(ps, dtype=np.float64))))


def underflow_length(p):
    """Smallest n with p**n == 0 in float64, multiplying step by step."""
    x, n = 1.0, 0
    while x > 0:
        x *= p
        n += 1
    return n

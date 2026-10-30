import numpy as np


def likelihood_product(ps):
    """Product of the probabilities in float64."""
    raise NotImplementedError


def log_likelihood_naive(ps):
    """log of the product (minus infinity once it underflows)."""
    raise NotImplementedError


def log_likelihood(ps):
    """Sum of the logs."""
    raise NotImplementedError


def underflow_length(p):
    """Smallest n with p**n == 0 in float64, multiplying step by step."""
    raise NotImplementedError

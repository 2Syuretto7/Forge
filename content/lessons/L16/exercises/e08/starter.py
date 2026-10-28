import numpy as np


def domain_epochs(weights, sizes, total_tokens):
    """How many times each domain is repeated when total_tokens are sampled with these weights."""
    raise NotImplementedError


def temperature_weights(sizes, tau):
    """Sampling weights proportional to size ** (1 / tau): tau = 1 samples by size, larger tau
    flattens toward uniform."""
    raise NotImplementedError


def mixture_objective(z, c, beta, T):
    """Mixture weights p = softmax(z); domain j's excess loss is c_j (p_j T)^-beta. Return the total
    sum_j c_j (p_j T)^-beta and its gradient with respect to z."""
    raise NotImplementedError


def optimal_mixture(c, beta):
    """The minimizer of sum_j c_j p_j^-beta subject to sum_j p_j = 1: p_j proportional to
    c_j ** (1 / (1 + beta))."""
    raise NotImplementedError

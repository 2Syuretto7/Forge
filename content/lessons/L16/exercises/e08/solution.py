import numpy as np


def domain_epochs(weights, sizes, total_tokens):
    """How many times each domain is repeated when total_tokens are sampled with these weights."""
    return np.asarray(weights) * total_tokens / np.asarray(sizes)


def temperature_weights(sizes, tau):
    """Sampling weights proportional to size ** (1 / tau): tau = 1 samples by size, larger tau
    flattens toward uniform."""
    w = np.asarray(sizes, dtype=float) ** (1 / tau)
    return w / w.sum()


def mixture_objective(z, c, beta, T):
    """Mixture weights p = softmax(z); domain j's excess loss is c_j (p_j T)^-beta. Return the total
    sum_j c_j (p_j T)^-beta and its gradient with respect to z."""
    e = np.exp(z - z.max())
    p = e / e.sum()
    L = c * (p * T) ** -beta
    dp = -beta * L / p
    return L.sum(), p * (dp - p @ dp)


def optimal_mixture(c, beta):
    """The minimizer of sum_j c_j p_j^-beta subject to sum_j p_j = 1: p_j proportional to
    c_j ** (1 / (1 + beta))."""
    w = np.asarray(c, dtype=float) ** (1 / (1 + beta))
    return w / w.sum()

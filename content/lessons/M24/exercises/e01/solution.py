import numpy as np


def markov_bound(mean, a):
    """Markov's bound on P(X >= a)."""
    return min(1.0, mean / a)


def chebyshev_bound(var, eps):
    """Chebyshev's bound on P(|X - mu| >= eps)."""
    return min(1.0, var / eps**2)


def tail_prob(samples, a):
    """Fraction of samples >= a."""
    return float(np.mean(np.asarray(samples) >= a))


def two_sided_prob(samples, mu, eps):
    """Fraction of samples with |x - mu| >= eps."""
    return float(np.mean(np.abs(np.asarray(samples) - mu) >= eps))

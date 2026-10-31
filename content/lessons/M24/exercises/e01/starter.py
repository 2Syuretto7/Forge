import numpy as np


def markov_bound(mean, a):
    """Markov's bound on P(X >= a)."""
    raise NotImplementedError


def chebyshev_bound(var, eps):
    """Chebyshev's bound on P(|X - mu| >= eps)."""
    raise NotImplementedError


def tail_prob(samples, a):
    """Fraction of samples >= a."""
    raise NotImplementedError


def two_sided_prob(samples, mu, eps):
    """Fraction of samples with |x - mu| >= eps."""
    raise NotImplementedError

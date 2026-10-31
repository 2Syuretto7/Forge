import numpy as np


def generate(P, start, n, T, rng):
    """Sample n tokens from a bigram table P (rows are next-token distributions) at temperature T,
    by rescaling log-probabilities: p_T proportional to P^(1/T)."""
    raise NotImplementedError


def distinct_ratio(seq, n=3):
    """Distinct n-grams divided by total n-grams: low values mean repetition."""
    raise NotImplementedError


def model_nll(seq, P):
    """Mean negative log-likelihood of a sequence under the untempered model."""
    raise NotImplementedError

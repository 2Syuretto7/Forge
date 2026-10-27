import numpy as np


def posterior(prior, likelihood):
    """Return the posterior over hypotheses, shape (H,)."""
    raise NotImplementedError


def positive_test_posterior(prevalence, sensitivity, false_positive_rate):
    """P(condition | positive test)."""
    raise NotImplementedError


def sequential(prior, likelihoods):
    """Apply Bayes' rule for each row of likelihoods (T, H). Return the final posterior."""
    raise NotImplementedError

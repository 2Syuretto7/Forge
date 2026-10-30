import numpy as np


def posterior(prior, likelihood):
    """Normalized prior times likelihood."""
    raise NotImplementedError


def positive_test_posterior(prevalence, sensitivity, false_positive_rate):
    """P(condition | positive test)."""
    raise NotImplementedError


def sequential(prior, likelihoods):
    """Apply Bayes' rule for each row of likelihoods."""
    raise NotImplementedError

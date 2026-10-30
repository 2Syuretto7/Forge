import numpy as np


def posterior(prior, likelihood):
    """Normalized prior times likelihood."""
    unnorm = np.asarray(prior, dtype=float) * np.asarray(likelihood, dtype=float)
    return unnorm / unnorm.sum()


def positive_test_posterior(prevalence, sensitivity, false_positive_rate):
    """P(condition | positive test)."""
    return float(posterior([prevalence, 1 - prevalence], [sensitivity, false_positive_rate])[0])


def sequential(prior, likelihoods):
    """Apply Bayes' rule for each row of likelihoods."""
    p = np.asarray(prior, dtype=float)
    for row in np.asarray(likelihoods, dtype=float):
        p = posterior(p, row)
    return p

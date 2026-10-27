import numpy as np


def posterior(prior, likelihood):
    """Return the posterior over hypotheses, shape (H,)."""
    unnorm = np.asarray(prior, dtype=float) * np.asarray(likelihood, dtype=float)
    return unnorm / unnorm.sum()


def positive_test_posterior(prevalence, sensitivity, false_positive_rate):
    """P(condition | positive test)."""
    post = posterior([prevalence, 1 - prevalence], [sensitivity, false_positive_rate])
    return float(post[0])


def sequential(prior, likelihoods):
    """Apply Bayes' rule for each row of likelihoods (T, H). Return the final posterior."""
    p = np.asarray(prior, dtype=float)
    for row in np.asarray(likelihoods, dtype=float):
        p = posterior(p, row)
    return p

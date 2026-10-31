import numpy as np


def neg_log_posterior(w, X, y, sigma, tau):
    """Negative log-posterior up to constants."""
    raise NotImplementedError


def ridge(X, y, lam):
    """Ridge regression."""
    raise NotImplementedError


def map_estimate(X, y, sigma, tau):
    """MAP estimate under a N(0, tau^2 I) prior and N(0, sigma^2) noise."""
    raise NotImplementedError

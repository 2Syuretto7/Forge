import numpy as np


def normal_logpdf(x, mu=0.0, sigma=1.0):
    """Log-density of N(mu, sigma^2)."""
    raise NotImplementedError


def is_estimate(f, logp, logq, xs):
    """Importance-sampling estimate of E_p[f] and its standard error."""
    raise NotImplementedError


def ess(w):
    """Effective sample size of a set of weights."""
    raise NotImplementedError

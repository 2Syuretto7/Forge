import numpy as np


def nll(mu, s, x):
    """Average negative log-likelihood of x under N(mu, exp(s)^2)."""
    raise NotImplementedError


def grad_nll(mu, s, x):
    """Return np.array([dJ/dmu, dJ/ds])."""
    raise NotImplementedError


def mle(x):
    """Return (mu_hat, sigma_hat) with the 1/n variance."""
    raise NotImplementedError

import math
import numpy as np


def nll(X, mu, Sigma):
    """Average negative log-likelihood of the rows of X."""
    raise NotImplementedError


def grad_mu(X, mu, Sigma):
    """Gradient of nll with respect to mu."""
    raise NotImplementedError


def mle(X):
    """Maximum-likelihood mean and covariance."""
    raise NotImplementedError

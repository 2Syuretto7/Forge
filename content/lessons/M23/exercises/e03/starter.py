import math
import numpy as np


def logpdf(X, mu, Sigma):
    """Log-density of N(mu, Sigma) at each row of X."""
    raise NotImplementedError


def score(X, mu, Sigma):
    """Gradient of the log-density at each row of X."""
    raise NotImplementedError

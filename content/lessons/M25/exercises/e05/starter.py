import math
import numpy as np

_lgamma = np.vectorize(math.lgamma)


def loglik(lam, x):
    """Poisson log-likelihood."""
    raise NotImplementedError


def score(lam, x):
    """Derivative of the log-likelihood with respect to lam."""
    raise NotImplementedError


def mle(x):
    """Maximum-likelihood estimate of lam."""
    raise NotImplementedError


def fisher_information(lam, n):
    """Expected information of n observations."""
    raise NotImplementedError


def standard_error(x):
    """Curvature-based standard error at the MLE."""
    raise NotImplementedError

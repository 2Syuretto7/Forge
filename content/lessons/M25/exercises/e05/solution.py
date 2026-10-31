import math
import numpy as np

_lgamma = np.vectorize(math.lgamma)


def loglik(lam, x):
    """Poisson log-likelihood."""
    x = np.asarray(x, dtype=float)
    return float(np.sum(x * np.log(lam) - lam - _lgamma(x + 1)))


def score(lam, x):
    """Derivative of the log-likelihood with respect to lam."""
    x = np.asarray(x, dtype=float)
    return float(np.sum(x) / lam - len(x))


def mle(x):
    """Maximum-likelihood estimate of lam."""
    return float(np.mean(x))


def fisher_information(lam, n):
    """Expected information of n observations."""
    return n / lam


def standard_error(x):
    """Curvature-based standard error at the MLE."""
    lam = mle(x)
    return 0.0 if lam == 0 else 1 / math.sqrt(fisher_information(lam, len(x)))

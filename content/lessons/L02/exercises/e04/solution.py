import numpy as np


def loglik(p, k, n):
    """k*log(p) + (n-k)*log(1-p) as a float, with 0*log(0) treated as 0."""
    out = 0.0
    if k > 0:
        out += k * np.log(p)
    if n - k > 0:
        out += (n - k) * np.log(1 - p)
    return float(out)


def dloglik(p, k, n):
    """Derivative of loglik with respect to p."""
    return k / p - (n - k) / (1 - p)


def mle(k, n):
    """Maximum likelihood estimate of p."""
    return k / n


def standard_error(k, n):
    """sqrt(p_hat * (1 - p_hat) / n)."""
    p = mle(k, n)
    return float(np.sqrt(p * (1 - p) / n))

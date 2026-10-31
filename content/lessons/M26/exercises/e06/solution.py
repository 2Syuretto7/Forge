import numpy as np


def naive_logsumexp(z):
    """log(sum(exp(z))) as written."""
    with np.errstate(over="ignore", divide="ignore"):
        return float(np.log(np.sum(np.exp(np.asarray(z, dtype=float)))))


def logsumexp(z):
    """Stable log(sum(exp(z)))."""
    z = np.asarray(z, dtype=float)
    m = z.max()
    return float(m + np.log(np.sum(np.exp(z - m))))


def softmax(z):
    """Stable softmax."""
    z = np.asarray(z, dtype=float)
    return np.exp(z - logsumexp(z))

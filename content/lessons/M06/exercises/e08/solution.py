import math


def logsumexp(z):
    """ln sum e**z_j, shifted by the maximum."""
    m = max(z)
    return m + math.log(sum(math.exp(v - m) for v in z))


def log_softmax(z):
    """z_i - LSE(z)."""
    lse = logsumexp(z)
    return [v - lse for v in z]


def nll(z, target):
    """Minus the log-softmax of the target class."""
    return -log_softmax(z)[target]

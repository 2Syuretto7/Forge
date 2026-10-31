import math


def log_mgf(t, p):
    """log(1 - p + p e^t)."""
    raise NotImplementedError


def d_log_mgf(t, p):
    """Derivative of log_mgf in t."""
    raise NotImplementedError


def chernoff_exponent(a, p):
    """sup over t >= 0 of t a - log M(t), by bisection."""
    raise NotImplementedError


def kl_bernoulli(a, p):
    """KL divergence between coins with probabilities a and p."""
    raise NotImplementedError


def chernoff_bound(n, a, p):
    """Chernoff's bound on P(mean >= a) for a > p."""
    raise NotImplementedError

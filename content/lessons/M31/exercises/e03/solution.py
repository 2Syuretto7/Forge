import math


def log_mgf(t, p):
    """log(1 - p + p e^t)."""
    return math.log(1 - p + p * math.exp(t))


def d_log_mgf(t, p):
    """Derivative of log_mgf in t."""
    return p * math.exp(t) / (1 - p + p * math.exp(t))


def chernoff_exponent(a, p):
    """sup over t >= 0 of t a - log M(t), by bisection."""
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if a - d_log_mgf(mid, p) > 0:
            lo = mid
        else:
            hi = mid
    t = 0.5 * (lo + hi)
    return t * a - log_mgf(t, p)


def kl_bernoulli(a, p):
    """KL divergence between coins with probabilities a and p."""
    return a * math.log(a / p) + (1 - a) * math.log((1 - a) / (1 - p))


def chernoff_bound(n, a, p):
    """Chernoff's bound on P(mean >= a) for a > p."""
    return math.exp(-n * chernoff_exponent(a, p))

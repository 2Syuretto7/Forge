import math
import numpy as np


def laplace_logpdf(x, b=1.0):
    """Log-density of the Laplace distribution with scale b."""
    return -np.abs(np.asarray(x, dtype=float)) / b - math.log(2 * b)


def laplace_sample(b, n, rng):
    """Laplace(0, b) samples by the inverse CDF."""
    u = rng.random(n)
    return np.where(u < 0.5, b * np.log(2 * np.maximum(u, 1e-300)), -b * np.log(2 * (1 - np.maximum(u, 0.5))))


def is_run(proposal, n, rng):
    """(estimate of E_p[X^2], standard error, ESS fraction) for the Laplace target."""
    if proposal == "normal":
        x = rng.standard_normal(n)
        logq = -0.5 * x * x - 0.5 * math.log(2 * math.pi)
    else:
        x = laplace_sample(2.0, n, rng)
        logq = laplace_logpdf(x, 2.0)
    w = np.exp(laplace_logpdf(x) - logq)
    v = x * x * w
    return float(v.mean()), float(v.std(ddof=1) / math.sqrt(n)), float(w.sum() ** 2 / np.sum(w * w) / n)

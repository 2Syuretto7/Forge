import numpy as np


def normal_logpdf(x, mu=0.0, sigma=1.0):
    """Log-density of N(mu, sigma^2)."""
    x = np.asarray(x, dtype=float)
    return -0.5 * ((x - mu) / sigma) ** 2 - np.log(sigma * np.sqrt(2 * np.pi))


def is_estimate(f, logp, logq, xs):
    """Importance-sampling estimate of E_p[f] and its standard error."""
    xs = np.asarray(xs, dtype=float)
    v = f(xs) * np.exp(logp(xs) - logq(xs))
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(xs)))


def ess(w):
    """Effective sample size of a set of weights."""
    w = np.asarray(w, dtype=float)
    return float(w.sum() ** 2 / np.sum(w * w))

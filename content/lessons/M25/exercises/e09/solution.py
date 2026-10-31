import math
import numpy as np


def beta_logpdf(t, a, b):
    """Log density of Beta(a, b) at points t in (0, 1)."""
    t = np.asarray(t, dtype=float)
    logB = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return (a - 1) * np.log(t) + (b - 1) * np.log1p(-t) - logB


def prob_a_better_grid(ka, na, kb, nb, m=20000):
    """P(theta_A > theta_B) under uniform priors, by numerical integration."""
    h = 1.0 / m
    t = (np.arange(m) + 0.5) * h
    pa = np.exp(beta_logpdf(t, 1 + ka, 1 + na - ka))
    pb = np.exp(beta_logpdf(t, 1 + kb, 1 + nb - kb))
    Fb = np.cumsum(pb) * h - 0.5 * pb * h
    return float(np.sum(pa * Fb) * h)


def prob_a_better_mc(ka, na, kb, nb, draws=200000, seed=0):
    """P(theta_A > theta_B) under uniform priors, by Monte Carlo."""
    rng = np.random.default_rng(seed)
    a = rng.beta(1 + ka, 1 + na - ka, size=draws)
    b = rng.beta(1 + kb, 1 + nb - kb, size=draws)
    return float(np.mean(a > b))

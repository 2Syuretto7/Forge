import numpy as np


def nll(mu, s, x):
    """Average negative log-likelihood of x under N(mu, exp(s)^2)."""
    x = np.asarray(x, dtype=float)
    return float(0.5 * np.log(2 * np.pi) + s + 0.5 * np.mean((x - mu) ** 2) * np.exp(-2 * s))


def grad_nll(mu, s, x):
    """Return np.array([dJ/dmu, dJ/ds])."""
    x = np.asarray(x, dtype=float)
    r = x - mu
    w = np.exp(-2 * s)
    return np.array([-np.mean(r) * w, 1.0 - np.mean(r * r) * w])


def mle(x):
    """Return (mu_hat, sigma_hat) with the 1/n variance."""
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(x.std())

import math
import numpy as np


def nll(w, s, X, y):
    """Average negative log-likelihood of a linear model with Gaussian noise."""
    r = np.asarray(y, dtype=float) - np.asarray(X, dtype=float) @ w
    return float(0.5 * math.log(2 * math.pi) + s + 0.5 * np.mean(r * r) * math.exp(-2 * s))


def grad_w(w, s, X, y):
    """Gradient of nll with respect to w."""
    X = np.asarray(X, dtype=float)
    r = np.asarray(y, dtype=float) - X @ w
    return -X.T @ r * math.exp(-2 * s) / len(r)


def fit(X, y):
    """Maximum-likelihood (w, sigma^2)."""
    w = np.linalg.lstsq(X, y, rcond=None)[0]
    r = y - X @ w
    return w, float(np.mean(r * r))

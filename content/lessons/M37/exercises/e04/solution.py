import numpy as np


def _logcomp(x, w, m, s):
    x = np.asarray(x, dtype=float)[:, None]
    m, s = np.asarray(m)[None], np.asarray(s)[None]
    return np.log(w)[None] - 0.5 * np.log(2 * np.pi * s**2) - (x - m) ** 2 / (2 * s**2)


def mixture_logpdf(x, w, m, s):
    """Log density of a one-dimensional Gaussian mixture."""
    L = _logcomp(x, w, m, s)
    mx = L.max(axis=1, keepdims=True)
    return (mx + np.log(np.sum(np.exp(L - mx), axis=1, keepdims=True)))[:, 0]


def responsibilities(x, w, m, s):
    """Posterior probability of each component."""
    L = _logcomp(x, w, m, s)
    L = L - L.max(axis=1, keepdims=True)
    R = np.exp(L)
    return R / R.sum(axis=1, keepdims=True)


def mixture_score(x, w, m, s):
    """Derivative of the log density."""
    x = np.asarray(x, dtype=float)
    R = responsibilities(x, w, m, s)
    return np.sum(R * (np.asarray(m)[None] - x[:, None]) / np.asarray(s)[None] ** 2, axis=1)

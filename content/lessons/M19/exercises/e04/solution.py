import numpy as np


def _softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def cross_entropy(z, c):
    """-log softmax(z)[c], computed stably."""
    m = z.max()
    return float(m + np.log(np.sum(np.exp(z - m))) - z[c])


def cross_entropy_grad(z, c):
    """p - y."""
    g = _softmax(z)
    g[c] -= 1.0
    return g


def chain_check(z, c):
    """Log VJP followed by softmax VJP."""
    p = _softmax(z)
    y = np.zeros_like(p)
    y[c] = 1.0
    pbar = -y / p
    return p * (pbar - pbar @ p)

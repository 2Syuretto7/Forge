import math
import numpy as np


# provided
def make_embeddings(n, seed=0, d=256):
    basis = np.linalg.qr(np.random.default_rng(1234).standard_normal((d, d)))[0]
    lam = 1.0 / np.arange(1, d + 1) + 0.01
    mean = np.random.default_rng(4321).normal(0, 0.5, d)
    z = np.random.default_rng(seed).standard_normal((n, d))
    return mean + (z * np.sqrt(lam)) @ basis.T


# provided
def gram(X, block=256):
    """X^T X accumulated over blocks of rows (fast in the browser)."""
    G = np.zeros((X.shape[1], X.shape[1]))
    for i in range(0, len(X), block):
        B = X[i:i + block]
        G += B.T @ B
    return G


def fit(X):
    """Maximum-likelihood mean and covariance."""
    raise NotImplementedError


def shrink(S, alpha):
    """Blend the covariance with a multiple of the identity."""
    raise NotImplementedError


def heldout_loglik(X_train, X_test, alpha=0.0):
    """Average log-density of X_test under the Gaussian fitted to X_train."""
    raise NotImplementedError

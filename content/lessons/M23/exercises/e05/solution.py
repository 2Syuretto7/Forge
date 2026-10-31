import numpy as np


def sample(mu, Sigma, n, rng):
    """n samples of N(mu, Sigma) by the Cholesky factor."""
    L = np.linalg.cholesky(np.asarray(Sigma, dtype=float))
    return np.asarray(mu, dtype=float) + rng.standard_normal((n, len(mu))) @ L.T


def whiten(X):
    """Cholesky whitening with the sample mean and covariance."""
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0)
    L = np.linalg.cholesky(np.cov(Xc, rowvar=False))
    return np.linalg.solve(L, Xc.T).T


def zca(X):
    """Symmetric (ZCA) whitening."""
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0)
    w, V = np.linalg.eigh(np.cov(Xc, rowvar=False))
    return Xc @ (V / np.sqrt(w)) @ V.T

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
    X = np.asarray(X, dtype=float)
    m = X.mean(axis=0)
    return m, gram(X - m) / len(X)


def shrink(S, alpha):
    """Blend the covariance with a multiple of the identity."""
    d = S.shape[0]
    return (1 - alpha) * S + alpha * np.trace(S) / d * np.eye(d)


def heldout_loglik(X_train, X_test, alpha=0.0):
    """Average log-density of X_test under the Gaussian fitted to X_train."""
    m, S = fit(X_train)
    L = np.linalg.cholesky(shrink(S, alpha))
    Z = np.linalg.solve(L, (np.asarray(X_test, dtype=float) - m).T)
    d = len(m)
    return float(np.mean(-0.5 * np.sum(Z * Z, axis=0)) - np.sum(np.log(np.diag(L))) - 0.5 * d * math.log(2 * math.pi))

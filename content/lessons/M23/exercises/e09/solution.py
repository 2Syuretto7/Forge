import math
import numpy as np


def nll(X, mu, Sigma):
    """Average negative log-likelihood of the rows of X."""
    X = np.asarray(X, dtype=float)
    L = np.linalg.cholesky(np.asarray(Sigma, dtype=float))
    Z = np.linalg.solve(L, (X - mu).T)
    d = X.shape[1]
    return float(0.5 * np.mean(np.sum(Z * Z, axis=0)) + np.sum(np.log(np.diag(L))) + 0.5 * d * math.log(2 * math.pi))


def grad_mu(X, mu, Sigma):
    """Gradient of nll with respect to mu."""
    X = np.asarray(X, dtype=float)
    return -np.linalg.solve(np.asarray(Sigma, dtype=float), X.mean(axis=0) - mu)


def mle(X):
    """Maximum-likelihood mean and covariance."""
    X = np.asarray(X, dtype=float)
    m = X.mean(axis=0)
    Xc = X - m
    return m, Xc.T @ Xc / len(X)

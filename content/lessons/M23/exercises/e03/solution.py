import math
import numpy as np


def logpdf(X, mu, Sigma):
    """Log-density of N(mu, Sigma) at each row of X."""
    X = np.atleast_2d(np.asarray(X, dtype=float))
    L = np.linalg.cholesky(np.asarray(Sigma, dtype=float))
    Z = np.linalg.solve(L, (X - mu).T)
    d = X.shape[1]
    return -0.5 * np.sum(Z * Z, axis=0) - np.sum(np.log(np.diag(L))) - 0.5 * d * math.log(2 * math.pi)


def score(X, mu, Sigma):
    """Gradient of the log-density at each row of X."""
    X = np.atleast_2d(np.asarray(X, dtype=float))
    return -np.linalg.solve(np.asarray(Sigma, dtype=float), (X - mu).T).T

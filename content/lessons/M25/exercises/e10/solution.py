import numpy as np


def neg_log_posterior(w, X, y, sigma, tau):
    """Negative log-posterior up to constants."""
    r = np.asarray(y, dtype=float) - np.asarray(X, dtype=float) @ w
    return float(r @ r / (2 * sigma**2) + w @ w / (2 * tau**2))


def ridge(X, y, lam):
    """Ridge regression."""
    X = np.asarray(X, dtype=float)
    return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ np.asarray(y, dtype=float))


def map_estimate(X, y, sigma, tau):
    """MAP estimate under a N(0, tau^2 I) prior and N(0, sigma^2) noise."""
    return ridge(X, y, sigma**2 / tau**2)

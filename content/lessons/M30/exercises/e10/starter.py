import numpy as np


# provided
def make_data(n=50000, d=10, seed=0):
    rng = np.random.default_rng(seed)
    w = rng.normal(size=d)
    X = rng.normal(size=(n, d))
    y = np.sign(X @ w + 0.5 * rng.normal(size=n))
    return X, y


def _primal(w, X, y, C):
    raise NotImplementedError


def relative_gap(alpha, X, y, C):
    """(P(w) - D(alpha)) / P(w) with w = X^T (alpha y)."""
    raise NotImplementedError


def train(X, y, C, tol=1e-4, max_iter=1500, check_every=25):
    """Accelerated projected gradient ascent on the SVM dual."""
    raise NotImplementedError

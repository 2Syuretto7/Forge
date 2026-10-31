import numpy as np


# provided
def make_task(n, d, seed=0):
    rng = np.random.default_rng(seed)
    w = np.random.default_rng(12345).normal(size=d) / np.sqrt(d) * 2
    X = rng.normal(size=(n, d))
    y = (rng.random(n) < 1 / (1 + np.exp(-X @ w))).astype(float)
    return X, y


def loss(w, X, y):
    """Average logistic loss."""
    raise NotImplementedError


def grad(w, X, y):
    """Gradient of the average logistic loss."""
    raise NotImplementedError


def fit(X, y, lam=1e-3, steps=300):
    """Gradient descent on the ridge-regularized logistic loss."""
    raise NotImplementedError


def gap(n, d, seed=0):
    """Test loss minus training loss."""
    raise NotImplementedError

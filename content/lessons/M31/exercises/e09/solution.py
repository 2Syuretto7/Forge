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
    z = X @ w
    return float(np.mean(np.maximum(z, 0) + np.log1p(np.exp(-np.abs(z))) - y * z))


def grad(w, X, y):
    """Gradient of the average logistic loss."""
    z = X @ w
    e = np.exp(-np.abs(z))
    s = np.where(z >= 0, 1 / (1 + e), e / (1 + e))
    return X.T @ (s - y) / len(y)


def fit(X, y, lam=1e-3, steps=300):
    """Gradient descent on the ridge-regularized logistic loss."""
    step = 4 * len(y) / np.linalg.eigvalsh(X.T @ X)[-1]
    w = np.zeros(X.shape[1])
    for _ in range(steps):
        w = w - step * (grad(w, X, y) + lam * w)
    return w


def gap(n, d, seed=0):
    """Test loss minus training loss."""
    X, y = make_task(n, d, seed)
    Xt, yt = make_task(5000, d, seed + 1000)
    w = fit(X, y)
    return loss(w, Xt, yt) - loss(w, X, y)

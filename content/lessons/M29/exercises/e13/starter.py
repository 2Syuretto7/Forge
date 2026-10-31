import numpy as np

# provided
_rng = np.random.default_rng(13)
# provided
X = _rng.normal(size=(500, 3))
# provided
y = (X @ np.array([2.0, -1.0, 1.0]) + _rng.logistic(size=500) > 0).astype(float)


# provided
def _sig(z):
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + e), e / (1 + e))


# provided
def loss(w):
    z = X @ w
    return float(np.mean(np.maximum(z, 0) + np.log1p(np.exp(-np.abs(z))) - y * z))


# provided
def grad(w):
    return X.T @ (_sig(X @ w) - y) / len(y)


# provided
def _newton():
    w = np.zeros(3)
    for _ in range(30):
        s = _sig(X @ w)
        H = X.T @ (X * (s * (1 - s))[:, None]) / len(y)
        w = w - np.linalg.solve(H, grad(w))
    return w


# provided
F_STAR = loss(_newton())


def sgd_constant(step, epochs, rng):
    """Full loss after each epoch of constant-step single-example SGD."""
    raise NotImplementedError


def sgd_decaying(step0, epochs, rng):
    """The same with step step0 / (1 + t / n)."""
    raise NotImplementedError


def gap_to_optimum(losses):
    """Last loss minus the optimum."""
    raise NotImplementedError

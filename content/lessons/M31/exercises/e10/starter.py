import numpy as np


# provided
def make_task(seed=0):
    rng = np.random.default_rng(seed)
    d, n, nt = 5, 100, 2000
    wt = rng.normal(size=d)
    X, Xt = rng.normal(size=(n, d)), rng.normal(size=(nt, d))
    y = np.sin(X @ wt) + 0.3 * rng.normal(size=n)
    yt = np.sin(Xt @ wt) + 0.3 * rng.normal(size=nt)
    W = rng.normal(size=(d, 200)) / np.sqrt(d)
    return X, y, Xt, yt, W


def ridge_loss(beta, F, y, lam):
    """Mean squared error plus lam |beta|^2."""
    raise NotImplementedError


def ridge_grad(beta, F, y, lam):
    """Gradient of ridge_loss."""
    raise NotImplementedError


def curves(lam=0.0):
    """Training and test errors for p = 1..200 random features."""
    raise NotImplementedError

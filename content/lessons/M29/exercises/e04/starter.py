import numpy as np

# provided
_rng = np.random.default_rng(4)
# provided
X = _rng.normal(size=(400, 5)) * np.array([1.0, 1.0, 3.0, 0.3, 2.0])
# provided
Y = (X @ np.array([0.5, -1.0, 0.3, 2.0, -0.4]) + _rng.normal(size=400) > 0).astype(float)


def nesterov(grad, x0, alpha, beta, iters):
    """Iterates of Nesterov's method with constant momentum."""
    raise NotImplementedError


def ridge_logistic(lam):
    """(f, grad) of the ridge-regularized logistic loss on X, Y."""
    raise NotImplementedError

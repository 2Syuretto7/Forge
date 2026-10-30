import numpy as np


# provided
def numerical_jacobian(f, x, h=1e-6):
    x = np.array(x, dtype=float)
    m = np.asarray(f(x)).size
    J = np.zeros((m, x.size))
    for j in range(x.size):
        e = np.zeros_like(x)
        e[j] = h
        J[:, j] = (np.asarray(f(x + e)) - np.asarray(f(x - e))) / (2 * h)
    return J


def jac_affine(W):
    """Jacobian of W x + b."""
    raise NotImplementedError


def jac_tanh(x):
    """Jacobian of elementwise tanh."""
    raise NotImplementedError


def jac_softmax(z):
    """Jacobian of the softmax."""
    raise NotImplementedError


def jac_polar(v):
    """Jacobian of (r, theta) -> (r cos theta, r sin theta)."""
    raise NotImplementedError


def jac_normalize(x):
    """Jacobian of x / |x|."""
    raise NotImplementedError

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
    return np.array(W, dtype=float)


def jac_tanh(x):
    """Jacobian of elementwise tanh."""
    return np.diag(1 - np.tanh(x) ** 2)


def jac_softmax(z):
    """Jacobian of the softmax."""
    p = np.exp(z - np.max(z))
    p /= p.sum()
    return np.diag(p) - np.outer(p, p)


def jac_polar(v):
    """Jacobian of (r, theta) -> (r cos theta, r sin theta)."""
    r, t = v
    return np.array([[np.cos(t), -r * np.sin(t)], [np.sin(t), r * np.cos(t)]])


def jac_normalize(x):
    """Jacobian of x / |x|."""
    n = np.linalg.norm(x)
    return (np.eye(x.size) - np.outer(x, x) / n ** 2) / n

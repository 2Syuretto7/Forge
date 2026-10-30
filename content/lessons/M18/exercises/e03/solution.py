import numpy as np


def numerical_jacobian(f, x, h=1e-6):
    """Central-difference Jacobian, shape (m, n)."""
    x = np.array(x, dtype=float)
    m = np.asarray(f(x)).size
    J = np.zeros((m, x.size))
    for j in range(x.size):
        e = np.zeros_like(x)
        e[j] = h
        J[:, j] = (np.asarray(f(x + e)) - np.asarray(f(x - e))) / (2 * h)
    return J


def jacobian_of_composition(Jg, Jf):
    """Jacobian of g(f(x))."""
    return Jg @ Jf

import numpy as np


def axis_check(f, x0, t=1e-2):
    """Whether f rises along every coordinate direction."""
    x0 = np.asarray(x0, dtype=float)
    base = f(x0)
    for i in range(x0.size):
        for s in (t, -t):
            e = np.zeros_like(x0)
            e[i] = s
            if f(x0 + e) <= base:
                return False
    return True


def hessian_eigen(H):
    """(eigenvalues, eigenvectors)."""
    return np.linalg.eigh(H)


def escape_direction(H):
    """Eigenvector of the most negative eigenvalue, or None."""
    w, V = np.linalg.eigh(H)
    return V[:, 0] if w[0] < 0 else None

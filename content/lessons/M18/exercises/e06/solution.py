import numpy as np


def hessian_from_grad(grad, x, h=1e-5):
    """Symmetrized central differences of the gradient."""
    x = np.array(x, dtype=float)
    n = x.size
    H = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = h
        H[:, j] = (grad(x + e) - grad(x - e)) / (2 * h)
    return 0.5 * (H + H.T)


def is_local_min(H, tol=1e-8):
    """All eigenvalues above tol."""
    return bool(np.all(np.linalg.eigvalsh(H) > tol))


def curvature_bound(H):
    """Largest eigenvalue."""
    return float(np.max(np.linalg.eigvalsh(H)))

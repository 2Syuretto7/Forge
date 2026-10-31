import numpy as np


def hessian_fd(f, x, h=1e-4):
    """Central-difference Hessian of f at x."""
    x = np.asarray(x, dtype=float)
    d = len(x)
    E = np.eye(d) * h
    H = np.zeros((d, d))
    for i in range(d):
        for j in range(d):
            H[i, j] = (f(x + E[i] + E[j]) - f(x + E[i] - E[j]) - f(x - E[i] + E[j]) + f(x - E[i] - E[j])) / (4 * h * h)
    return (H + H.T) / 2


def min_eigenvalue(H):
    """Smallest eigenvalue of a symmetric matrix."""
    return float(np.linalg.eigvalsh(np.asarray(H, dtype=float))[0])


def convex_on_samples(f, points, h=1e-4, tol=1e-6):
    """Whether the Hessian is positive semidefinite at every sample point."""
    return all(min_eigenvalue(hessian_fd(f, p, h)) > -tol for p in points)

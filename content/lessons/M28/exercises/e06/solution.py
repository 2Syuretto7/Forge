import numpy as np


def make_quadratic(eigs, seed):
    """Symmetric matrix with the given eigenvalues and random eigenvectors."""
    d = len(eigs)
    Q, _ = np.linalg.qr(np.random.default_rng(seed).standard_normal((d, d)))
    return Q @ np.diag(eigs) @ Q.T


def gd_errors(A, b, x0, step, iters):
    """Error norms of gradient descent on (1/2) x^T A x - b^T x."""
    xs = np.linalg.solve(A, b)
    x = np.array(x0, dtype=float)
    out = [np.linalg.norm(x - xs)]
    for _ in range(iters):
        x = x - step * (A @ x - b)
        out.append(np.linalg.norm(x - xs))
    return np.array(out)


def rate(eigs, step):
    """Worst contraction factor of gradient descent."""
    return float(np.max(np.abs(1 - step * np.asarray(eigs, dtype=float))))

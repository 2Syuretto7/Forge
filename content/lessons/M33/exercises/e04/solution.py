import numpy as np


def quadratic(A, b, x):
    """f(x) = x^T A x / 2 - b^T x."""
    return 0.5 * x @ A @ x - b @ x


def grad_quadratic(A, b, x):
    """Gradient of the quadratic."""
    return A @ x - b


def cg(matvec, b, tol=1e-10, max_iter=None):
    """Conjugate gradient from zero: (x, residual norms, directions)."""
    b = np.asarray(b, dtype=float)
    n = len(b)
    max_iter = max_iter or 10 * n
    x = np.zeros(n)
    r = b.copy()
    p = r.copy()
    rr = r @ r
    norms = [np.sqrt(rr)]
    dirs = []
    for _ in range(max_iter):
        Ap = matvec(p)
        a = rr / (p @ Ap)
        x = x + a * p
        r = r - a * Ap
        dirs.append(p)
        rr_new = r @ r
        norms.append(np.sqrt(rr_new))
        if norms[-1] <= tol * norms[0]:
            break
        p = r + (rr_new / rr) * p
        rr = rr_new
    return x, norms, dirs

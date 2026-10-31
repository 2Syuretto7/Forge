import numpy as np


def pcg(A, b, minv, tol=1e-8, max_iter=5000):
    """Jacobi-preconditioned conjugate gradient: (x, iterations)."""
    x = np.zeros(len(b))
    r = np.array(b, dtype=float)
    z = minv * r
    p = z.copy()
    rz = r @ z
    target = tol * np.linalg.norm(b)
    for k in range(1, max_iter + 1):
        Ap = A @ p
        a = rz / (p @ Ap)
        x += a * p
        r -= a * Ap
        if np.linalg.norm(r) <= target:
            return x, k
        z = minv * r
        new = r @ z
        p = z + (new / rz) * p
        rz = new
    return x, max_iter


def badly_scaled(n, rng, spread=1e4):
    """A well-conditioned matrix with badly scaled variables."""
    G = rng.standard_normal((n, n))
    A0 = G @ G.T / n + np.eye(n)
    d = np.geomspace(1 / np.sqrt(spread), np.sqrt(spread), n)
    return d[:, None] * A0 * d[None, :]


def jacobi_condition(A):
    """Condition number after symmetric diagonal scaling."""
    s = 1 / np.sqrt(np.diag(A))
    return float(np.linalg.cond(s[:, None] * A * s[None, :]))

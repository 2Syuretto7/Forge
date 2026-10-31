import numpy as np


# provided
def make_nonsymmetric(n, rng):
    G = rng.standard_normal((n, n))
    S = G @ G.T / n + np.eye(n)
    return S + 0.4 * np.triu(rng.standard_normal((n, n)), 1)


def cg_residuals(A, b, iters):
    """Relative residuals of plain CG, whatever A is."""
    x = np.zeros(len(b))
    r = np.array(b, dtype=float)
    p = r.copy()
    rr = r @ r
    nb = np.linalg.norm(b)
    out = []
    for _ in range(iters):
        Ap = A @ p
        d = p @ Ap
        if d == 0:
            break
        a = rr / d
        x += a * p
        r -= a * Ap
        new = r @ r
        out.append(float(np.sqrt(new) / nb))
        p = r + (new / rr) * p
        rr = new
    return out


def cgnr(A, b, tol=1e-10, max_iter=5000):
    """CG on the normal equations: (x, iterations)."""
    c = A.T @ b
    x = np.zeros(A.shape[1])
    r = c.copy()
    p = r.copy()
    rr = r @ r
    target = tol * np.sqrt(rr)
    for k in range(1, max_iter + 1):
        Ap = A.T @ (A @ p)
        a = rr / (p @ Ap)
        x += a * p
        r -= a * Ap
        new = r @ r
        if np.sqrt(new) <= target:
            return x, k
        p = r + (new / rr) * p
        rr = new
    return x, max_iter

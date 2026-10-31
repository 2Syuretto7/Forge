import numpy as np


def heavy_ball(A, b, x0, alpha, beta, iters):
    """Error norms of heavy-ball momentum on (1/2) x^T A x - b^T x."""
    xs = np.linalg.solve(A, b)
    x = np.array(x0, dtype=float)
    prev = x.copy()
    out = [np.linalg.norm(x - xs)]
    for _ in range(iters):
        x, prev = x - alpha * (A @ x - b) + beta * (x - prev), x
        out.append(np.linalg.norm(x - xs))
    return np.array(out)


def optimal_heavy_ball(L, mu):
    """Optimal step and momentum for a quadratic."""
    k = L / mu
    return 4 / (np.sqrt(L) + np.sqrt(mu)) ** 2, ((np.sqrt(k) - 1) / (np.sqrt(k) + 1)) ** 2

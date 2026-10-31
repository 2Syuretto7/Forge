import numpy as np


def project_box(y, lo, hi):
    """Closest point of the box [lo, hi]^n."""
    return np.clip(np.asarray(y, dtype=float), lo, hi)


def project_ball(y, r):
    """Closest point of the ball of radius r."""
    y = np.asarray(y, dtype=float)
    n = np.linalg.norm(y)
    return y if n <= r else y * (r / n)


def project_simplex(y):
    """Closest point of the probability simplex."""
    y = np.asarray(y, dtype=float)
    u = np.sort(y)[::-1]
    css = np.cumsum(u) - 1
    k = np.arange(1, len(y) + 1)
    rho = np.nonzero(u - css / k > 0)[0][-1]
    return np.maximum(y - css[rho] / (rho + 1), 0)


def projected_gd(grad, proj, x0, step, iters):
    """Projected gradient descent; returns the last iterate."""
    x = proj(np.asarray(x0, dtype=float))
    for _ in range(iters):
        x = proj(x - step * grad(x))
    return x

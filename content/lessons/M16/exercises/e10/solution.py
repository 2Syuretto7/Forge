import numpy as np


def newton_cbrt_vec(a, iters):
    """Vectorized Newton for cube roots."""
    x = np.where(a >= 1, a, 1.0).astype(float)
    for _ in range(iters):
        x = 2 * x / 3 + a / (3 * x * x)
    return x


def steps_to_converge(a, method, tol=1e-15):
    """Vectorized steps until every element is accurate."""
    target = np.cbrt(a)
    if method == "newton":
        x = np.where(a >= 1, a, 1.0).astype(float)
        for k in range(1, 500):
            x = 2 * x / 3 + a / (3 * x * x)
            if np.all(np.abs(x - target) <= tol * target):
                return k
        return None
    lo, hi = np.zeros_like(a, dtype=float), np.maximum(1.0, a).astype(float)
    for k in range(1, 500):
        m = (lo + hi) / 2
        up = m ** 3 < a
        lo, hi = np.where(up, m, lo), np.where(up, hi, m)
        if np.all(np.abs((lo + hi) / 2 - target) <= tol * target):
            return k
    return None

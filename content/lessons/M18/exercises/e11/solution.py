import numpy as np


def directional_check(f, grad, x, k=5, h=1e-4, seed=0):
    """Worst relative difference over k random directions."""
    rng = np.random.default_rng(seed)
    g = grad(x)
    worst = 0.0
    for _ in range(k):
        u = rng.normal(size=x.size)
        u /= np.linalg.norm(u)
        a = float(g @ u)
        b = (f(x + h * u) - f(x - h * u)) / (2 * h)
        worst = max(worst, abs(a - b) / max(abs(a), abs(b), 1e-12))
    return worst


def buggy_grad(grad, i):
    """grad with entry i doubled."""
    def g(x):
        v = np.array(grad(x), dtype=float)
        v[i] *= 2
        return v
    return g

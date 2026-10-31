import numpy as np


def grid_mean(f, d, k):
    """Midpoint-rule average of f over k^d grid points in the unit cube."""
    pts = (np.arange(k) + 0.5) / k
    G = np.stack(np.meshgrid(*[pts] * d, indexing="ij"), axis=-1).reshape(-1, d)
    return float(np.mean(f(G)))


def mc_mean(f, d, n, rng):
    """Monte Carlo average of f over n uniform points in the unit cube."""
    return float(np.mean(f(rng.random((n, d)))))

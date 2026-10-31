import numpy as np


def rademacher_linear(X, B, draws, rng):
    """Monte Carlo estimate of the empirical Rademacher complexity."""
    X = np.asarray(X, dtype=float)
    S = rng.choice([-1.0, 1.0], size=(draws, len(X)))
    return float(B * np.mean(np.linalg.norm(S @ X, axis=1)) / len(X))


def rademacher_bound(X, B):
    """B sqrt(sum |x_i|^2) / n."""
    X = np.asarray(X, dtype=float)
    return float(B * np.sqrt(np.sum(X * X)) / len(X))

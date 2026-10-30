import numpy as np


def fraction_small_det(n, t, seed=0):
    """Fraction of n random 2x2 matrices (entries uniform in [-1, 1]) with |det| < t."""
    A = np.random.default_rng(seed).uniform(-1, 1, size=(n, 2, 2))
    det = A[:, 0, 0] * A[:, 1, 1] - A[:, 0, 1] * A[:, 1, 0]
    return float(np.mean(np.abs(det) < t))


def amplification(A, b, eps=1e-6):
    """Largest movement of the solution per unit nudge of b, over four axis nudges."""
    x = np.linalg.solve(A, b)
    nudges = [np.array([eps, 0.0]), np.array([-eps, 0.0]), np.array([0.0, eps]), np.array([0.0, -eps])]
    return max(np.linalg.norm(np.linalg.solve(A, b + n) - x) for n in nudges) / eps

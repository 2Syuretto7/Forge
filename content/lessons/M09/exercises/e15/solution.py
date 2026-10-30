import numpy as np


def cosine_distance(x, y):
    """1 - cos(angle)."""
    return float(1 - x @ y / (np.linalg.norm(x) * np.linalg.norm(y)))


def angular_distance(x, y):
    """The angle in radians."""
    c = np.clip(x @ y / (np.linalg.norm(x) * np.linalg.norm(y)), -1.0, 1.0)
    return float(np.arccos(c))


def triangle_violation(D, x, y, z):
    """D(x, z) - D(x, y) - D(y, z)."""
    return D(x, z) - D(x, y) - D(y, z)


def find_violation(D, trials=1000, seed=0):
    """A random triple of plane unit vectors violating the triangle inequality, or None."""
    rng = np.random.default_rng(seed)
    for _ in range(trials):
        a = rng.uniform(0, 2 * np.pi, size=3)
        x, y, z = (np.array([np.cos(t), np.sin(t)]) for t in a)
        if triangle_violation(D, x, y, z) > 1e-9:
            return x, y, z
    return None

import numpy as np


def shell_fraction(n, eps):
    """Fraction of volume within eps of the surface."""
    return 1 - (1 - eps) ** n


def sample_ball(n, m, seed=0):
    """Uniform points in the unit ball."""
    rng = np.random.default_rng(seed)
    G = rng.normal(size=(m, n))
    G /= np.linalg.norm(G, axis=1, keepdims=True)
    return G * rng.random(m)[:, None] ** (1 / n)


def mean_radius(n, m=100_000, seed=0):
    """Average distance from the centre."""
    return float(np.mean(np.linalg.norm(sample_ball(n, m, seed), axis=1)))

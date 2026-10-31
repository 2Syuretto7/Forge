import numpy as np


def mp_edges(gamma):
    """Edges of the Marchenko-Pastur support."""
    r = np.sqrt(gamma)
    return (1 - r) ** 2, (1 + r) ** 2


def mp_density(x, gamma):
    """Marchenko-Pastur density for variance 1 and ratio gamma <= 1."""
    a, b = mp_edges(gamma)
    x = np.asarray(x, dtype=float)
    inside = (x > a) & (x < b)
    safe = np.where(inside, x, 1.0)
    val = np.sqrt(np.clip((b - safe) * (safe - a), 0, None)) / (2 * np.pi * gamma * safe)
    return np.where(inside, val, 0.0)


def sample_cov_eigs(n, p, rng):
    """Eigenvalues of the sample covariance of n standard normal samples."""
    X = rng.standard_normal((n, p))
    return np.linalg.eigvalsh(X.T @ X / n)


def mp_moments(gamma):
    """First two moments of the Marchenko-Pastur law."""
    return 1.0, 1.0 + gamma

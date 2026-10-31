import math
import numpy as np


# provided
def gram(X, block=256):
    """X^T X accumulated over blocks of rows (fast in the browser)."""
    G = np.zeros((X.shape[1], X.shape[1]))
    for i in range(0, len(X), block):
        B = X[i:i + block]
        G += B.T @ B
    return G


def sample_cov_spectrum(n, d, seed):
    """Eigenvalues of the sample covariance of n standard normal vectors."""
    X = np.random.default_rng(seed).standard_normal((n, d))
    return np.linalg.eigvalsh(gram(X) / n)


def mp_edges(n, d):
    """Marchenko-Pastur edges (1 -/+ sqrt(d/n))^2."""
    g = math.sqrt(d / n)
    return max(0.0, 1 - g) ** 2, (1 + g) ** 2


def spectral_error(n, d, seed):
    """Largest absolute eigenvalue of S - I."""
    e = sample_cov_spectrum(n, d, seed)
    return float(max(e[-1] - 1, 1 - e[0]))

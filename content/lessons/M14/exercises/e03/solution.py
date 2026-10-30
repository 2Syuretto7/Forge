import numpy as np


def singular_values_2x2(A):
    """(sigma_1, sigma_2) from the eigenvalues of A^T A."""
    G = A.T @ A
    p, q, r = G[0, 0], G[0, 1], G[1, 1]
    m, d = (p + r) / 2, np.hypot((p - r) / 2, q)
    return float(np.sqrt(m + d)), float(np.sqrt(max(m - d, 0.0)))


def circle_image_extremes(A, n=3600):
    """Largest and smallest |A x| over n points of the unit circle."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    L = np.linalg.norm(A @ np.vstack([np.cos(t), np.sin(t)]), axis=0)
    return float(L.max()), float(L.min())


def area_factor(A):
    """|det A|."""
    return float(abs(A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]))

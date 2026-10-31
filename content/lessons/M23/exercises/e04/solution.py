import numpy as np


def ellipse_axes(Sigma):
    """(eigenvalues decreasing, eigenvectors as columns)."""
    w, V = np.linalg.eigh(np.asarray(Sigma, dtype=float))
    return w[::-1], V[:, ::-1]


def mahalanobis(X, mu, Sigma):
    """Mahalanobis distance of each row of X."""
    D = np.atleast_2d(np.asarray(X, dtype=float)) - mu
    return np.sqrt(np.sum(D * np.linalg.solve(np.asarray(Sigma, dtype=float), D.T).T, axis=1))


def prob_inside(k):
    """P(r <= k) for a 2D Gaussian."""
    return 1 - np.exp(-k * k / 2)


def ellipse_points(mu, Sigma, k, m=100):
    """Points on the contour r = k."""
    w, V = ellipse_axes(Sigma)
    t = np.linspace(0, 2 * np.pi, m, endpoint=False)
    circle = np.stack([np.cos(t), np.sin(t)], axis=1)
    return np.asarray(mu, dtype=float) + (circle * (k * np.sqrt(w))) @ V.T

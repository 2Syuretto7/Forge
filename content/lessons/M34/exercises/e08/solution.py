import numpy as np


def spiked_samples(n, p, ell, rng):
    """Samples with one planted direction of variance 1 + ell."""
    X = rng.standard_normal((n, p))
    X[:, 0] *= np.sqrt(1 + ell)
    return X


def top_eig_and_overlap(X):
    """Top eigenvalue of X^T X / n and its eigenvector's squared overlap with e_1."""
    vals, vecs = np.linalg.eigh(X.T @ X / len(X))
    return float(vals[-1]), float(vecs[0, -1] ** 2)


def bbp_top(ell, gamma):
    """Predicted top eigenvalue."""
    return (1 + ell) * (1 + gamma / ell) if ell > np.sqrt(gamma) else (1 + np.sqrt(gamma)) ** 2


def bbp_overlap(ell, gamma):
    """Predicted squared overlap of the top eigenvector with the planted direction."""
    return (1 - gamma / ell**2) / (1 + gamma / ell) if ell > np.sqrt(gamma) else 0.0

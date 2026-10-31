import numpy as np


# provided
def planted_matrix(n, p, strengths, rng):
    W = rng.standard_normal((n, p))
    for s in strengths:
        u = rng.standard_normal(n)
        v = rng.standard_normal(p)
        W += np.sqrt(s) * np.outer(u, v / np.linalg.norm(v))
    return W


def top_eigenvalue(S):
    """Largest eigenvalue of a symmetric matrix."""
    return float(np.linalg.eigvalsh(S)[-1])


def grad_top_eigenvalue(S):
    """Gradient of the largest eigenvalue: v v^T."""
    v = np.linalg.eigh(S)[1][:, -1]
    return np.outer(v, v)


def count_outliers(W, margin=1.05):
    """Eigenvalues of W^T W / n above the Marchenko-Pastur edge."""
    n, p = W.shape
    edge = (1 + np.sqrt(p / n)) ** 2
    return int(np.sum(np.linalg.eigvalsh(W.T @ W / n) > margin * edge))

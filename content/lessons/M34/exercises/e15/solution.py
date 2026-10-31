import numpy as np


def anisotropic(n, d, common, rng):
    """Rows sharing a common component of length common * sqrt(d)."""
    m = rng.standard_normal(d)
    m *= common * np.sqrt(d) / np.linalg.norm(m)
    return m + rng.standard_normal((n, d))


def mean_pairwise_cosine(X):
    """Average cosine over all pairs of rows."""
    U = X / np.linalg.norm(X, axis=1, keepdims=True)
    G = U @ U.T
    i, j = np.triu_indices(len(X), 1)
    return float(G[i, j].mean())


def center(X):
    """Subtract the mean row."""
    return X - X.mean(axis=0)


def predicted_cosine(common):
    """Typical cosine between rows with a shared component."""
    return common**2 / (common**2 + 1)

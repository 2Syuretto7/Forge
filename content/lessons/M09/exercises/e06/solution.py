import numpy as np


def normalize_rows(X):
    """Each row divided by its length."""
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def cosine_matrix(X):
    """(n, n) cosine similarities between rows."""
    U = normalize_rows(X)
    return U @ U.T


def most_similar_pair(X):
    """(i, j), i < j, with the largest cosine."""
    C = cosine_matrix(X)
    i, j = np.triu_indices(len(X), k=1)
    k = int(np.argmax(C[i, j]))
    return int(i[k]), int(j[k])

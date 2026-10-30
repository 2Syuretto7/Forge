import numpy as np


# provided
def make_corpus(seed=0, n=20000, d=48, topics=40, n_queries=20):
    """Unit embeddings around topic directions, and queries near random documents."""
    rng = np.random.default_rng(seed)
    centers = rng.normal(size=(topics, d))
    centers /= np.linalg.norm(centers, axis=1, keepdims=True)
    labels = rng.integers(0, topics, size=n)
    X = centers[labels] + 0.35 * rng.normal(size=(n, d)) / np.sqrt(d) * 4
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    picks = rng.integers(0, n, size=n_queries)
    Q = X[picks] + 0.1 * rng.normal(size=(n_queries, d))
    Q /= np.linalg.norm(Q, axis=1, keepdims=True)
    return X.astype(np.float64), Q


def kmeans(X, n_clusters, iters, seed=0):
    """Spherical k-means: (centroids, assignment)."""
    raise NotImplementedError


def build(X, n_clusters=64, iters=10, seed=0):
    """IVF index: centroids and the row indices of each cluster."""
    raise NotImplementedError


def search(index, X, q, k=5, n_probe=8):
    """(top-k row indices, vectors scanned) probing the n_probe nearest clusters."""
    raise NotImplementedError


def exact_search(X, q, k=5):
    """Brute-force top-k by cosine."""
    raise NotImplementedError


def recall(found, exact):
    """Mean fraction of exact neighbours found, over queries."""
    raise NotImplementedError

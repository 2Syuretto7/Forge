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
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), size=n_clusters, replace=False)].copy()
    assign = np.zeros(len(X), dtype=int)
    for _ in range(iters):
        assign = np.argmax(X @ C.T, axis=1)
        for j in range(n_clusters):
            members = X[assign == j]
            if len(members):
                m = members.mean(axis=0)
                C[j] = m / np.linalg.norm(m)
    return C, assign


def build(X, n_clusters=64, iters=10, seed=0):
    """IVF index: centroids and the row indices of each cluster."""
    C, assign = kmeans(X, n_clusters, iters, seed)
    return {"centroids": C, "lists": [np.flatnonzero(assign == j) for j in range(n_clusters)]}


def search(index, X, q, k=5, n_probe=8):
    """(top-k row indices, vectors scanned) probing the n_probe nearest clusters."""
    probe = np.argsort(-(index["centroids"] @ q))[:n_probe]
    rows = np.concatenate([index["lists"][j] for j in probe])
    s = X[rows] @ q
    top = rows[np.argsort(-s)[:k]]
    return [int(i) for i in top], len(rows)


def exact_search(X, q, k=5):
    """Brute-force top-k by cosine."""
    return [int(i) for i in np.argsort(-(X @ q))[:k]]


def recall(found, exact):
    """Mean fraction of exact neighbours found, over queries."""
    return float(np.mean([len(set(f) & set(e)) / len(e) for f, e in zip(found, exact)]))

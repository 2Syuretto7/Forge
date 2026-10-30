# Capstone: a semantic search toy

The starter's `make_corpus(seed)` returns 20,000 unit-length embeddings in 48 dimensions (documents about 40 topics) and 20 queries. Build an **inverted file (IVF) index**:

1. `kmeans(X, n_clusters, iters, seed)`: spherical k-means. Start from `n_clusters` rows chosen at random; repeat `iters` times: assign every vector to the centroid with the largest cosine, then set each centroid to the normalized mean of its vectors (keep an empty cluster's old centroid). Return the centroids and the assignment.
2. `build(X, n_clusters=64, iters=10, seed=0)`: run k-means and return an index: a dictionary with `"centroids"`, and `"lists"`, a list giving the row indices of each cluster.
3. `search(index, X, q, k=5, n_probe=8)`: score the query against all centroids, take the `n_probe` most similar clusters, compute cosines only with their vectors, and return the top `k` row indices together with the number of vectors scanned.
4. `exact_search(X, q, k=5)`: the brute-force reference.
5. `recall(found, exact)`: the fraction of the exact neighbours that were found, averaged over queries.

The tests require recall@5 of at least 0.9 over the 20 queries, while scanning at most 25 percent of the database on average.

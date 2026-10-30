# Nearest neighbours by brute force

- `top_k(query, X, k)`: the indices of the `k` rows of `X` with the largest cosine similarity to `query`, in decreasing order of similarity.
- `top_k_euclidean(query, X, k)`: the `k` rows nearest to `query` in Euclidean distance, nearest first.
- `same_order_when_normalized(query, X, k)`: whether the two methods return the same indices when `X`'s rows and the query are first normalized to unit length. They should: for unit vectors $\|q - x\|^2 = 2 - 2\,q \cdot x$, so a smaller distance is a larger cosine.

## Hints

1. Compute all cosines with a matrix-vector product, then `np.argsort(-scores)[:k]`.
2. `np.linalg.norm(X - query, axis=1)`, then `np.argsort(...)[:k]`.
3. Normalize both before comparing.

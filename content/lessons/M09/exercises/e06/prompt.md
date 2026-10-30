# A cosine-similarity matrix

For a matrix `X` of shape `(n, d)` with one vector per row:

- `normalize_rows(X)`: each row divided by its length (as a new array).
- `cosine_matrix(X)`: the `(n, n)` array of cosine similarities between every pair of rows, computed as one matrix product of the normalized rows with their transpose.
- `most_similar_pair(X)`: the pair `(i, j)` with `i < j` whose cosine is largest.

## Hints

1. `X / np.linalg.norm(X, axis=1, keepdims=True)`.
2. `U @ U.T`.
3. Ignore the diagonal (a row's similarity with itself is 1): use `np.triu_indices(n, k=1)`.

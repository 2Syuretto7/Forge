# Normalize once, search many

A real index answers many queries. Precompute what does not depend on the query.

- `build_index(X)`: the normalized database (float32), computed once.
- `batch_search(index, Q, k)`: for a matrix `Q` of queries (one per row), the `(len(Q), k)` integer array of top-`k` indices for every query, from **one** matrix product `index @ Qn.T` (or its transpose) for all queries at once.
- `flops_per_query(n, d)`: the multiply-adds counted as 2 FLOPs each: $2nd$.

## Hints

1. Normalize the queries too.
2. `np.argpartition` works along an axis: `axis=1`.
3. Sort each row's `k` candidates by score with `np.take_along_axis`.

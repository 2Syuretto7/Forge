# Vectorized search over 100,000 vectors

- `make_database(n, d, seed=0)`: `n` random vectors of length `d` as a float32 array of shape `(n, d)` with standard normal entries.
- `search_loop(query, X, k)`: the indices of the top `k` cosine similarities, computed with a Python loop over rows (one dot product per row, with `float(X[i] @ query)`), for timing comparison.
- `search_vectorized(query, X, k)`: the same with one matrix-vector product and `np.argpartition` to find the top `k` without sorting everything, then sorting just those `k`.
- `speedup(n, d, k=5)`: the time of `search_loop` divided by the time of `search_vectorized` on a database of `n` vectors (time each with `time.perf_counter`; repeat the fast one until it takes at least 20 ms).

The tests check that the two searches agree and that vectorizing is at least 10 times faster.

## Hints

1. Normalize the rows once; then cosine is a plain dot product.
2. `idx = np.argpartition(-s, k)[:k]`, then sort `idx` by `-s[idx]`.
3. The loop is slow on purpose: use `n = 20000` in experiments.

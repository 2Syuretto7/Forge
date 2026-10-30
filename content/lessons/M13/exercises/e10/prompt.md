# PageRank without a dense matrix

Store a graph as two integer arrays, `src` and `dst`, one entry per link.

- `make_graph(n, k=10, seed=0)`: each page gets `k` links to targets $\lfloor n u^3 \rfloor$ for uniform $u$ (low-numbered pages are popular), except that every twentieth page (indices divisible by 20) has none. Return `(src, dst)`.
- `step(src, dst, outdeg, x, d)`: one application of the Google matrix without forming it: follow links with `np.bincount(dst, weights=x[src] / outdeg[src], minlength=n)`, spread the probability on pages without links and the teleport evenly.
- `pagerank_sparse(src, dst, n, d=0.85, tol=1e-10, max_iter=1000)`: return `(x, residuals)`, where `residuals` lists the sum of absolute changes at each step.

Then run `pagerank_sparse` on `make_graph(100000)` in the console: about a million links, a few seconds.

## Hints

1. `outdeg = np.bincount(src, minlength=n)`; pages with `outdeg == 0` are dangling.
2. The teleport and dangling parts add the same number to every page: $(d \cdot \text{dangling mass} + 1 - d) / n$.
3. The result must still sum to 1 at every step; test that.

# The smallest singular value collapses at p = n

Measure Section 5's explanation of the peak.

- `sigma_min(n, p, seed)`: the smallest singular value of an `n x p` matrix of independent standard normals drawn with `np.random.default_rng(seed).normal(size=(n, p))` (the smallest of the $\min(n, p)$ singular values).
- `sigma_min_curve(n, ps, trials, seed)`: the average over `trials` matrices (seeds `seed`, `seed + 1`, ...) for each `p` in `ps`.
- `mp_edge(n, p)`: the prediction $|\sqrt p - \sqrt n|$.

## Hints

1. `np.linalg.svd(A, compute_uv=False)[-1]`.
2. Average over trials to smooth the curve.
3. The approximation is good for large matrices away from $p = n$.

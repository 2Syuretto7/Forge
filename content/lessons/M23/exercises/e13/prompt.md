# Break it: fewer samples than dimensions

With $n$ samples in $d > n$ dimensions, the centered data span at most $n - 1$ directions, so the sample covariance is singular: it claims zero variance in every other direction, and the Gaussian it defines has no density.

- `sample_cov_rank(n, d, seed, tol=1e-10)`: the number of eigenvalues of the sample covariance (with $n - 1$) above `tol` times the largest, for `n` standard normal samples in `d` dimensions.
- `cholesky_with_jitter(S, start=1e-10, factor=10, max_tries=20)`: try the Cholesky factor of $S + jI$ for `j = 0`, then `start`, `start * factor`, and so on, up to `max_tries` jitters; return `(L, j)` for the first that succeeds, and raise `np.linalg.LinAlgError` if none does.

Desktop NumPy raises `LinAlgError` when a matrix is not positive definite; the browser's NumPy returns a factor full of NaNs instead. The starter's `try_cholesky(S)` handles both and returns `None` on failure.

The tests show the rank stuck at $n - 1$, plain Cholesky failing, and the jitter making it succeed.

## Hints

1. `np.cov(X, rowvar=False)` and `np.linalg.eigvalsh`.
2. Loop over the jitters and stop at the first `try_cholesky` that is not `None`.
3. Jitter is a tiny version of e11's shrinkage: it adds a little variance in every direction.

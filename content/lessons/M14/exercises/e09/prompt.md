# Two norms from the singular values

- `spectral_norm(A)`: $\sigma_1$.
- `frobenius_from_s(A)`: $\sqrt{\sum_i \sigma_i^2}$.
- `stretch_samples(A, k=2000, seed=0)`: the largest $\|Ax\|$ over `k` random unit vectors $x$.

The tests check an **invariant** for random matrices: the Frobenius norm from the singular values equals the square root of the sum of the squared entries, no sampled stretch exceeds $\sigma_1$, and $\sigma_1 \leq \|A\|_F \leq \sqrt{r}\,\sigma_1$ for rank $r$.

## Hints

1. `np.linalg.svd(A, compute_uv=False)`.
2. Rotations do not change the sum of squares, so $\|U\Sigma V^\top\|_F = \|\Sigma\|_F$.
3. Normalize random Gaussian vectors to get random unit vectors.

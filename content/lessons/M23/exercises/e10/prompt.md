# How good is a sample covariance in 256 dimensions?

Draw $n$ samples from $N(0, I_{256})$ and form $S = \frac1n X^\top X$ (the mean is known to be 0). Every eigenvalue of the truth is 1, but the eigenvalues of $S$ spread out. For $d/n = \gamma$, random matrix theory (the **Marchenko-Pastur law**) predicts that they fill the interval from $(1 - \sqrt\gamma)^2$ to $(1 + \sqrt\gamma)^2$.

- `sample_cov_spectrum(n, d, seed)`: the eigenvalues of $S$ in increasing order, from `np.random.default_rng(seed).standard_normal((n, d))`.
- `mp_edges(n, d)`: the predicted smallest and largest eigenvalue, the smallest clipped at 0.
- `spectral_error(n, d, seed)`: $\lVert S - I\rVert_2$, the largest absolute eigenvalue of $S - I$.

The tests check the edges at $n = 256$, 1,024, 4,096 and 8,192 within 10 percent, and that the error shrinks like $\sqrt{d/n}$: four times the data, half the error.

## Hints

1. `np.linalg.eigvalsh(gram(X) / n)`. The starter's `gram(X)` computes $X^\top X$ in blocks of 256 rows: the browser's NumPy has no optimized matrix library, and a product with an inner dimension of thousands runs ten times faster cut into blocks that fit in the cache.
2. At $n = d$ the smallest eigenvalue is about 0: the matrix is nearly singular although it is built from as many samples as dimensions.
3. $\lVert S - I\rVert_2 = \max(\lambda_{\max} - 1,\ 1 - \lambda_{\min})$.

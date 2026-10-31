# Sampling by Cholesky, and whitening

Section 4: if $z$ is standard normal and $\Sigma = LL^\top$, then $x = \mu + Lz$ has covariance $LL^\top = \Sigma$. Running the map backwards **whitens** data: it removes the correlations and equalizes the variances.

- `sample(mu, Sigma, n, rng)`: `n` rows from $N(\mu, \Sigma)$, using `rng.standard_normal`.
- `whiten(X)`: subtract the sample mean and apply $L^{-1}$, where $LL^\top$ is the sample covariance; the result has exactly the identity as sample covariance.
- `zca(X)`: the symmetric whitening $\Sigma^{-1/2}(x - \bar x)$, with $\Sigma^{-1/2} = V\,\mathrm{diag}(\lambda^{-1/2})V^\top$ from the eigendecomposition.

The tests check both whitenings and that ZCA changes the data least: among all whitenings it stays closest to the centered data.

## Hints

1. Rows times a transposed factor: `mu + Z @ L.T`.
2. `np.linalg.solve(L, Xc.T).T` applies $L^{-1}$ to every row.
3. Use the sample covariance with $n - 1$, `np.cov(X, rowvar=False)`.

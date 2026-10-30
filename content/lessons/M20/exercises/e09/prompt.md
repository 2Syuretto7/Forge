# Gaussians in n dimensions

- `normalizer(Sigma)`: $(2\pi)^{n/2}\sqrt{\det\Sigma}$.
- `gaussian_density(x, Sigma)`: $\exp(-\frac12 x^\top\Sigma^{-1}x)$ divided by the normalizer (use `np.linalg.solve`, not an inverse).
- `sample_gaussian(Sigma, n, seed=0)`: `n` samples as rows, by $x = Lz$ with $L$ the Cholesky factor of $\Sigma$ and $z$ standard normal.

The tests integrate the two-dimensional density on a grid and compare the sample covariance with $\Sigma$.

## Hints

1. `np.linalg.det` and `math.pi`.
2. `x @ np.linalg.solve(Sigma, x)`.
3. With samples as rows, `Z @ L.T`.

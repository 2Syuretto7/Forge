# Mean vector and covariance matrix

Data arrive as the rows of an `(n, d)` array (Section 2).

- `mean_and_cov(X)`: the mean vector and the sample covariance matrix $\frac{1}{n-1}\sum_i (x_i - \bar x)(x_i - \bar x)^\top$.
- `var_of_combination(cov, a)`: the variance of $a^\top x$, which is $a^\top \Sigma a$.
- `affine_moments(mu, cov, A, b)`: the mean and covariance of $Ax + b$: $A\mu + b$ and $A\Sigma A^\top$.
- `correlation_matrix(cov)`: $\Sigma_{ij}/\sqrt{\Sigma_{ii}\Sigma_{jj}}$.

The tests compare with `np.cov`, check that the sample variance of $Xa$ equals $a^\top S a$ exactly, and that every covariance matrix has nonnegative eigenvalues.

## Hints

1. Center first: `Xc = X - X.mean(axis=0)`, then `Xc.T @ Xc / (n - 1)`.
2. `a @ cov @ a`.
3. `s = np.sqrt(np.diag(cov))`, then `cov / np.outer(s, s)`.

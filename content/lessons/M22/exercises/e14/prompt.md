# Break it: adding variances that are not independent

"Variances add" needs the terms to be uncorrelated. For $n$ variables with covariance matrix $\Sigma$, the variance of their sum is $\mathbf 1^\top \Sigma \mathbf 1$, the sum of every entry, while the independent formula keeps only the diagonal.

- `var_sum_independent(cov)`: the sum of the variances, the trace.
- `var_sum(cov)`: the correct variance of the sum.
- `equicorrelated(n, rho, sigma=1.0)`: the covariance matrix with $\sigma^2$ on the diagonal and $\rho\sigma^2$ everywhere else.
- `effective_n(n, rho)`: how many independent samples give the mean of $n$ equicorrelated ones the same variance, $n / (1 + (n - 1)\rho)$.

The tests sample correlated variables and show the independent formula off by a factor of about 11 at $n = 100$, $\rho = 0.1$: a hundred measurements worth nine.

## Hints

1. `cov.sum()` is $\mathbf 1^\top \Sigma \mathbf 1$.
2. `sigma**2 * ((1 - rho) * np.eye(n) + rho)`.
3. The variance of the mean of $n$ equicorrelated variables is $\sigma^2 (1 + (n - 1)\rho)/n$; set it equal to $\sigma^2/n_{\text{eff}}$.

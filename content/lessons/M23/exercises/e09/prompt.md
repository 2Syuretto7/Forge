# Fitting a Gaussian by maximum likelihood

The average negative log-likelihood of data rows $x_i$ under $N(\mu, \Sigma)$ is

$$
\text{nll}(\mu, \Sigma) = \frac{1}{n}\sum_i \tfrac12 (x_i - \mu)^\top \Sigma^{-1} (x_i - \mu) + \tfrac12\log\det\Sigma + \tfrac d2\log 2\pi .
$$

- `nll(X, mu, Sigma)`: that average, with the log-determinant from the Cholesky factor.
- `grad_mu(X, mu, Sigma)`: its gradient with respect to $\mu$, $-\Sigma^{-1}(\bar x - \mu)$.
- `mle(X)`: the minimizer, the sample mean and the covariance with $\frac1n$ (not $\frac{1}{n-1}$).

The tests run a **gradient check** of `grad_mu` and confirm that perturbing the fitted mean or covariance in any direction increases the loss.

## Hints

1. $\log\det\Sigma = 2\sum_i \log L_{ii}$.
2. The gradient vanishes exactly at $\mu = \bar x$, whatever $\Sigma$ is.
3. `np.cov(X, rowvar=False, bias=True)` divides by $n$.

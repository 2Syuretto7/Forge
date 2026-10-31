# Least squares as maximum likelihood

Fit $y = Xw + \epsilon$ with Gaussian noise (Section 1). `X` is `(n, d)` and already contains a column of ones if you want an intercept.

- `ols(X, y)`: the least-squares weights, via `np.linalg.lstsq`.
- `gaussian_nll(w, sigma, X, y)`: the average negative log-likelihood $\tfrac12\log(2\pi\sigma^2) + \tfrac{1}{2\sigma^2}\cdot\text{mean}((y - Xw)^2)$.
- `noise_mle(X, y, w)`: the MLE of $\sigma^2$ given `w`, the mean squared residual.

The tests confirm that `ols` minimizes `gaussian_nll` for every fixed `sigma` and that the variance MLE maximizes the likelihood.

## Hints

1. `np.linalg.lstsq(X, y, rcond=None)[0]`.
2. Write the residual once: `r = y - X @ w`.
3. The variance MLE divides by $n$.

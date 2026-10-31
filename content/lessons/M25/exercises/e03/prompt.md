# The coin's log-likelihood, its gradient and its MLE

For $k$ heads in $n$ flips, implement the log-likelihood $\ell(p) = k\log p + (n-k)\log(1-p)$ (without the constant $\log\binom{n}{k}$), its derivative from Section 2, the MLE, and the standard error from the curvature.

- `loglik(p, k, n)` returns a float.
- `dloglik(p, k, n)` returns $\ell'(p)$.
- `mle(k, n)` returns $\hat p$.
- `standard_error(k, n)` returns $\sqrt{\hat p(1-\hat p)/n}$.

The gradient test compares `dloglik` with central differences.

## Hints

1. $\ell'(p) = k/p - (n-k)/(1-p)$.
2. Handle `k = 0` and `k = n` in `loglik` by treating $0 \log 0$ as 0: use `np.where` or check the counts.
3. The standard error is the square root of the negative inverse curvature at $\hat p$.

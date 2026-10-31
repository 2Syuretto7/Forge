# The maximum-likelihood rate is biased

For exponential waiting times with rate $\lambda$, the MLE of the mean $1/\lambda$ is $\bar x$, and by the **invariance** of maximum likelihood the MLE of the rate is $\hat\lambda = 1/\bar x$. The mean is unbiased; its reciprocal is not: $\mathbb{E}[1/\bar x] = \frac{n}{n - 1}\lambda$ (Section 1).

- `rate_mle(x)`: $1/\bar x$.
- `rate_unbiased(x)`: $(n - 1)/\sum_i x_i$.
- `simulate_rate_bias(n, lam, trials, seed)`: draw `np.random.default_rng(seed).exponential(1 / lam, size=(trials, n))`, apply both estimators to every row, and return their average minus $\lambda$.

The tests compare with the predicted bias $\lambda/(n - 1)$ of the MLE.

## Hints

1. A function of an unbiased estimator is unbiased only if the function is linear; $1/x$ is convex, so by Jensen's inequality (M28) $\mathbb{E}[1/\bar x] > 1/\mathbb{E}\bar x$.
2. Row means: `X.mean(axis=1)`.
3. The bias vanishes like $1/n$, faster than the standard error, which shrinks like $1/\sqrt n$.

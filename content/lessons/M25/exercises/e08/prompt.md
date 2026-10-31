# Beta priors, MAP and credible intervals

Implement Section 5 for a coin with a $\text{Beta}(a, b)$ prior and $k$ heads in $n$ flips.

- `posterior_params(a, b, k, n)` returns `(alpha, beta)` of the Beta posterior.
- `map_estimate(a, b, k, n)` returns the posterior mode (assume $\alpha, \beta > 1$).
- `posterior_mean(a, b, k, n)`.
- `credible_interval(alpha, beta, level, draws, seed)`: an equal-tailed interval from `draws` Monte Carlo samples of `np.random.default_rng(seed).beta(alpha, beta, size=draws)`. Return `(lo, hi)`.

## Hints

1. Conjugacy: add the heads to $a$ and the tails to $b$.
2. The mode of $\text{Beta}(\alpha, \beta)$ is $(\alpha - 1)/(\alpha + \beta - 2)$.
3. `np.quantile(samples, [(1 - level) / 2, (1 + level) / 2])`.

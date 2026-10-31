# Measuring the bias of variance estimators

Check Section 1 by simulation.

- `variance_estimators(x)` returns `(biased, unbiased)`: the sum of squared deviations from the sample mean divided by $n$ and by $n - 1$.
- `simulate_bias(n, sigma, trials, seed)`: draw `trials` samples of size `n` from $\mathcal{N}(0, \sigma^2)$ with `np.random.default_rng(seed).normal(0, sigma, size=(trials, n))`, apply both estimators to every row (vectorized), and return `(bias_biased, bias_unbiased)`: the average estimate minus $\sigma^2$.

The tests compare with the theoretical bias $-\sigma^2/n$ and $0$.

## Hints

1. `np.var(x, ddof=0)` and `np.var(x, ddof=1)`.
2. Pass `axis=1` to estimate per row.
3. With 200,000 trials the Monte Carlo error in the average is small but not zero; the tests allow for it.

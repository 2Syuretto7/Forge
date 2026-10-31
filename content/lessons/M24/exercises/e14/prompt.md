# Break it: the central limit theorem without a variance

The Pareto distribution with $\alpha = 1.5$ and $x_m = 1$ has mean $\alpha/(\alpha - 1) = 3$ but infinite variance. The sample standard deviation still produces a number, so the interval $\bar x \pm 1.96\,s/\sqrt n$ can still be computed. It is wrong.

- `pareto(alpha, size, rng)`: inverse-CDF samples $(1 - U)^{-1/\alpha}$ with one call `rng.random(size)`; `size` may be a tuple.
- `coverage(samples, true_mean)`: `samples` has shape `(runs, n)`; the fraction of rows whose CLT interval contains `true_mean`.

The tests compare 2,000 intervals from samples of 100: about 94 percent coverage for the exponential, and below 85 percent for the Pareto, whose rare huge values sometimes inflate the mean and usually are missing, making it too small with an error bar that is too short.

## Hints

1. `(1 - rng.random(size)) ** (-1 / alpha)`.
2. Reuse e04's interval with `axis=1`.
3. The median of the Pareto sample means is below 3: most samples miss the tail that carries the mean.

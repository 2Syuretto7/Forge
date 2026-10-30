# The mean as the best guess

If you must guess $X$ with one number $c$ and pay the squared error, the expected cost is $\text{mse}(c) = \mathbb{E}[(X - c)^2]$. Expanding gives $\text{mse}(c) = \operatorname{Var}X + (\mathbb{E}X - c)^2$: the mean is the best guess, and the variance is the cost that remains.

- `mse(c, values, probs)` and `dmse_dc(c, values, probs)`, its derivative $-2\,\mathbb{E}[X - c]$.
- `best_constant(values, probs)`: the minimizer of `mse`.
- `mae(c, values, probs)`: $\mathbb{E}\lvert X - c\rvert$.
- `best_constant_abs(values, probs)`: a minimizer of `mae`, a median: the smallest value whose cumulative probability, after sorting, reaches $\frac12$.

The tests run a **gradient check** of `dmse_dc`, confirm the decomposition, and compare the two best guesses on a skewed distribution.

## Hints

1. `np.sum(probs * (values - c) ** 2)`.
2. The derivative is $2(c - \mathbb{E}X)$: zero exactly at the mean.
3. Sort the values with `np.argsort`, carry the probabilities along, and use `np.cumsum`.

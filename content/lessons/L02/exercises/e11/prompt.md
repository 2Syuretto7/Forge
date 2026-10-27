# Break it: heavy tails defeat the sample mean

The law of large numbers and the CLT need finite variance. Show what happens without it.

- `iqr(v)`: the interquartile range, $q_{0.75} - q_{0.25}$, of a 1-D array.
- `spread_of_means(samples)`: `samples` has shape `(trials, n)`; return the IQR of the `trials` row means.
- `spread_of_medians(samples)`: the same for row medians.

The tests draw Gaussian and Cauchy data at $n = 10$ and $n = 1000$. For the Gaussian, the spread of means shrinks by about $\sqrt{100} = 10$. For the Cauchy, the spread of means does not shrink at all, while the spread of medians still does.

## Hints

1. `np.quantile(v, 0.75) - np.quantile(v, 0.25)`.
2. Use `axis=1` for row means and medians.
3. The mean of $n$ standard Cauchy draws is itself standard Cauchy, whose IQR is exactly 2.

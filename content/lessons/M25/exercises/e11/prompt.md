# The bootstrap and its coverage

Implement the percentile bootstrap of Section 7 and measure how often its intervals contain the truth.

- `bootstrap_means(x, B, seed)`: draw `B` resamples of `x` with replacement using `np.random.default_rng(seed).integers(0, n, size=(B, n))` and return the `B` resample means.
- `percentile_ci(stats, level)`: the equal-tailed percentile interval `(lo, hi)`.
- `coverage(true_mean, datasets, B, level, seed)`: `datasets` has shape `(R, n)`. For each row, build a percentile interval for the mean (use seed `seed + r` for row `r`) and return the fraction of rows whose interval contains `true_mean`.

A 95 percent interval should contain the truth about 95 percent of the time. Percentile bootstrap intervals for small samples tend to come in a little low; the test accepts 0.90 to 0.98.

## Hints

1. Index `x[idx]` with the `(B, n)` integer array, then `.mean(axis=1)`.
2. `np.quantile(stats, [(1 - level) / 2, (1 + level) / 2])`.
3. Coverage is a mean of booleans.

# Confidence intervals and their coverage

By the central limit theorem, $\bar x \pm 1.96\,s/\sqrt n$ contains the true mean in about 95 percent of repetitions (Section 3).

- `normal_interval(values, z=1.96)`: `(low, high)` around the sample mean, with $s$ the sample standard deviation (`ddof=1`).
- `coverage(draw, true_mean, n, runs, rng)`: call `draw(rng, (runs, n))` once to get `runs` samples of size `n`, build an interval for each row, and return the fraction that contain `true_mean`.
- `n_for_halfwidth(sigma, h, z=1.96)`: the smallest $n$ with $z\sigma/\sqrt n \le h$.

The tests check about 95 percent coverage for exponential data, and that a halfwidth of 0.01 for a standard deviation of 1 needs 38,416 samples.

## Hints

1. Compute all the row means and standard deviations at once with `axis=1`.
2. A row covers the truth when `low <= true_mean <= high`.
3. $n = \lceil (z\sigma/h)^2 \rceil$; round slightly before taking the ceiling.

# How sure is the exponent?

A scaling exponent fitted to a handful of runs is uncertain, and the uncertainty grows with the distance you extrapolate. The bootstrap (L02) estimates it without any distributional assumptions.

Implement `bootstrap_exponent(x, y, n_boot=1000, seed=0, level=0.9)`: with `np.random.default_rng(seed)`, draw `n_boot` resamples of the runs with replacement (`rng.integers(0, n, n)`), skip any with fewer than two distinct runs, refit $y = k x^{-a}$ in log-log coordinates, and return the central `level` percentile interval of $a$.

## Hints

1. Resample indices and use them for both $x$ and $y$, so each run keeps its pair.
2. `np.quantile(values, [(1 - level) / 2, (1 + level) / 2])`.
3. Spreading the same number of runs over a wider range of $x$ shrinks the interval.

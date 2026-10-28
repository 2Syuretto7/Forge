# An evaluation harness with error bars

A validation loss is an average over examples, and has sampling error. Comparing two checkpoints on the same examples, the paired difference is far more precise than comparing their separate intervals.

1. `mean_with_ci(values, n_boot=2000, seed=0, level=0.95)`: the mean and a percentile bootstrap interval. Draw all resamples at once with `rng.integers(0, n, (n_boot, n))`.
2. `paired_difference(a, b, ...)`: the mean of $a - b$ over the same examples, with its interval.

## Hints

1. Use `np.random.default_rng(seed)`.
2. Resample examples, keeping each pair together; resampling $a$ and $b$ separately throws away the pairing.
3. Two runs whose intervals overlap can still differ clearly: check the interval of the difference.

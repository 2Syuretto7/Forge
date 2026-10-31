# Accuracy with an error bar

A benchmark score is an average over items, a sample from the space of possible questions. Report it with an interval.

1. `accuracy_ci(correct, n_boot=2000, seed=0, level=0.95)`: the accuracy over items (0/1) and a percentile bootstrap interval that resamples items (M25).
2. `standard_error(p, n)`: $\sqrt{p(1-p)/n}$.

## Hints

1. Draw all resamples at once: `c[rng.integers(0, n, (n_boot, n))]`.
2. For accuracies not near 0 or 1, the bootstrap interval is close to $p \pm 1.96$ standard errors.
3. Items, not tokens or runs, are the unit to resample: they are what the benchmark sampled.

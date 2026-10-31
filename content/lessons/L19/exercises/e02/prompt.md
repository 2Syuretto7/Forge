# Comparing two models fairly

Two models answered the same items. Their separate intervals overlap more than the evidence warrants: items vary in difficulty, and both models find the same items hard. Compare them item by item.

Implement `paired_bootstrap(a, b, n_boot=2000, seed=0, level=0.95)`: the mean of $a - b$ over items and a bootstrap interval that resamples items, keeping each pair together.

## Hints

1. Compute the per-item differences first, then bootstrap their mean.
2. An interval that excludes 0 means the difference is unlikely to be sampling noise.
3. The tests build two models that share most of their mistakes.

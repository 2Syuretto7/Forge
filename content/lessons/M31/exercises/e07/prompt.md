# A guaranteed interval and a likely one

A classifier's correctness on $n$ test examples is a 0/1 vector. Report its accuracy two ways (Section 1, and M25):

- `hoeffding_interval(correct, delta=0.05)`: `(accuracy, low, high)` with half-width $\sqrt{\ln(2/\delta)/(2n)}$: guaranteed, for any distribution, as long as the examples are independent.
- `bootstrap_interval(correct, B=2000, seed=0, level=0.95)`: `(accuracy, low, high)` from percentiles of resampled accuracies: approximate, and much narrower when the accuracy is near 0 or 1.
- `width_ratio(correct)`: Hoeffding's width over the bootstrap's.

The tests find the two intervals agreeing on the center, Hoeffding wider (about 2.5 times at 92 percent accuracy, because it ignores the small variance $p(1 - p)$), and both containing the truth.

## Hints

1. Resample by counts, as in M25: for 0/1 values, `rng.binomial(n, acc, size=B) / n`.
2. `np.quantile(boot, [(1 - level) / 2, (1 + level) / 2])`.
3. Hoeffding's width does not depend on the accuracy at all; the bootstrap's is about $2 \times 1.96\sqrt{p(1 - p)/n}$.

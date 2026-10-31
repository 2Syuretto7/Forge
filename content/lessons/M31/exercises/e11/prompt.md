# How conservative is Hoeffding?

Simulate 10,000 independent test sets of 1,000 examples for a classifier with true accuracy $0.92$, and count how often each interval contains the truth.

- `coverage(intervals, truth)`: the fraction of `(low, high)` rows with `low <= truth <= high`.
- `hoeffding_intervals(accs, n, delta=0.05)` and `clt_intervals(accs, n, z=1.96)`: arrays of `(low, high)` rows for an array of measured accuracies.
- `simulate(p, n, sets, rng)`: the measured accuracies of `sets` test sets, from `rng.binomial(n, p, size=sets) / n`.

The tests find the CLT interval covering about 95 percent of the time, as advertised, and Hoeffding's about 100 percent: a guarantee for every distribution on $[0, 1]$ costs width on any particular one.

## Hints

1. `np.column_stack([accs - h, accs + h])`.
2. The CLT interval uses the measured accuracy in $\sqrt{a(1 - a)/n}$.
3. Hoeffding's half-width here is about five of the binomial's standard deviations.

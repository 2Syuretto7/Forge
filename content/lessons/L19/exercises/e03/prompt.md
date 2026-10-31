# How many items?

1. `items_needed(p, half_width, z=1.96)`: the items needed for an interval of $\pm$ `half_width` around an accuracy near $p$: $n = z^2 p (1 - p) / h^2$, rounded up.
2. `detectable_difference(p, n, z=1.96)`: roughly the smallest difference between two independent evaluations of $n$ items each that a 95% test detects, $z\sqrt{2p(1-p)/n}$.

## Hints

1. Halving the interval needs four times the items.
2. Accuracies near 50% need the most items.
3. Many leaderboard gaps of a point or two on benchmarks of a few hundred items are within noise.

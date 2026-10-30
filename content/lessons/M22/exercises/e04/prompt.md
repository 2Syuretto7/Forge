# Linearity of expectation with indicators

The expectation of a sum is the sum of expectations, whether or not the terms are independent. Writing a count as a sum of indicators, one per possible event, turns hard questions into easy ones (Section 2).

- `expected_fixed_points(n)`: the expected number of cards that stay in place when $n$ cards are shuffled uniformly at random.
- `simulate_fixed_points(n, trials, seed)`: shuffle `trials` times with `np.random.default_rng(seed)` and return the average number of fixed points.
- `expected_empty_bins(balls, bins)`: throw `balls` balls independently and uniformly into `bins` bins; the expected number of empty bins.
- `expected_distinct_birthdays(n, days=365)`: the expected number of distinct birthdays among $n$ people.

## Hints

1. Card $i$ stays in place with probability $1/n$.
2. A bin is empty with probability $(1 - 1/\text{bins})^{\text{balls}}$.
3. Random permutations in bulk: `np.argsort(rng.random((trials, n)), axis=1)`.

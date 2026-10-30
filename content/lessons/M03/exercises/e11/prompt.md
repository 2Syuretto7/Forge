# How long did each falsehood survive?

Given the results of the hunter (name to `(counterexample, tried)`), summarize the false claims.

- `survival_times(results)`: the sorted list of `tried` values for the claims that were refuted.
- `median(xs)`: the middle value of a sorted list (the mean of the two middle values for an even length).
- `longest_survivor(results)`: the name of the refuted claim that took the most tries (the first such name in alphabetical order if there is a tie).
- `share_within(results, k)`: the fraction of refuted claims that broke within `k` tries.

The starter provides `RESULTS`, the hunter's output for the fifty claims with a limit of 60, so this exercise does not depend on the previous one.

## Hints

1. `sorted(t for ce, t in results.values() if ce is not None)`.
2. For an even length `m`, average `xs[m // 2 - 1]` and `xs[m // 2]`.
3. `max(sorted(names), key=...)` returns the first maximum in alphabetical order.

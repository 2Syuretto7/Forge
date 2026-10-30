# Fifty claims

The starter defines `CLAIMS`: fifty classic claims, each a dictionary with a `"name"`, a `"claim"` (a predicate of a whole number $n$) and a `"start"` (the first $n$ to try). Twenty-five are true and twenty-five are false.

Write `run_hunter(claims, limit)`. For each claim, try $n$ = `start`, `start + 1`, ... up to `start + limit - 1`, and record what happened. Return a dictionary from each claim's name to a pair `(counterexample, tried)`: the first $n$ where the claim fails (or `None`), and how many values of $n$ were tried.

Then write `broken(results)`, the sorted list of names whose claims were refuted, and `survivors(results)`, the sorted list of the rest.

## Hints

1. Reuse your `hunt_count` from the build movement, with `range(start, start + limit)` as the cases.
2. `sorted(name for name, (ce, _) in results.items() if ce is not None)`.
3. Surviving the limit does not make a claim true. With a limit of 60, two false claims survive; the tests then run a longer hunt. One of them fails first at 341 = 11 x 31, a composite number that divides $2^{341} - 2$ just as primes do.

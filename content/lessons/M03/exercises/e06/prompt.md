# A counterexample hunter

A claim is a predicate: a function returning `True` when the claim holds for that case.

- `hunt(claim, cases)`: try the cases in order and return the first one where the claim is `False`, or `None` if it survives them all.
- `hunt_count(claim, cases)`: return the pair `(counterexample, tried)`: the first counterexample (or `None`) and how many cases were checked, including the counterexample itself.
- `hunt_pairs(claim, xs)`: for a claim about two values, try every pair `(a, b)` from `xs` (in order, `a` slowest) and return the first failing pair or `None`.

## Hints

1. `for i, x in enumerate(cases)` gives you the position too.
2. If no counterexample turns up, `tried` is the number of cases.
3. Two nested loops for pairs.

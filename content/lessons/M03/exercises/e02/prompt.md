# Equivalence, tautologies and satisfiability

- `equivalent(f, g, n)`: `True` when the formulas agree on every one of the $2^n$ rows.
- `tautology(f, n)`: `True` when `f` is true on every row (such as $p$ or not $p$).
- `satisfiable(f, n)`: `True` when `f` is true on at least one row.
- `counterexamples(f, g, n)`: the list of input rows where `f` and `g` disagree.

For finitely many true-or-false inputs, checking every row is a complete proof: there are no other cases. The tests include an **invariant**: for many randomly built formulas, De Morgan's law holds and every formula is equivalent to itself.

## Hints

1. Loop over `itertools.product([True, False], repeat=n)`.
2. `satisfiable(f, n)` is `not tautology(lambda *x: not f(*x), n)`; check that your two definitions agree.
3. A row is a tuple; call the formula with `f(*row)`.

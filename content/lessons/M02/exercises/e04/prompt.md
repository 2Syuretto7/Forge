# Check a step at random points

A claimed step turns expression `before` into expression `after`. If both are the same function of their variables, they agree everywhere both are defined. Write:

- `same_function(e1, e2, names, trials=50, seed=0)`: draw `trials` random points (each variable uniform between -10 and 10, using `random.Random(seed)`), evaluate both expressions, and return `False` as soon as they disagree by more than `1e-9 * max(1, abs(value))`. Skip any point where either expression raises `ZeroDivisionError` (a point outside its domain). Return `True` if no point disagrees.
- `counterexample(e1, e2, names, trials=200, seed=0)`: the first point (a dictionary of variable values) where they disagree, or `None`.

The starter provides `evaluate` from the first exercise.

The tests include an **invariant**: an expression always agrees with itself, and with its own copy after rewriting by the distributive law.

## Hints

1. `rnd = random.Random(seed)`, then `{v: rnd.uniform(-10, 10) for v in names}`.
2. Wrap the two evaluations in `try: ... except ZeroDivisionError: continue`.
3. `counterexample` is `same_function` that returns the point instead of `False`.

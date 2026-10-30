# Capstone: a step-checked algebra notebook

The starter defines `NOTEBOOK`, a list of fifteen derivations. Each derivation is a dictionary with a `"title"`, the `"names"` of its variables, and its `"steps"`: a list of expression trees, each claimed equal to the one before. Thirteen derivations are correct; two contain one wrong step each.

Write:

- `evaluate(expr, env)` for trees as in the build movement;
- `agree(e1, e2, names, trials=60, seed=0)`: `True` when the two expressions agree at every random point where both are defined (values uniform in $[-5, 5]$; skip points that raise `ZeroDivisionError`; tolerance `1e-9 * max(1, abs(value))`);
- `first_bad_step(steps, names)`: the index of the first step that does not agree with the step before it, or `None`;
- `audit(notebook)`: a list of `(derivation index, step index)` pairs, one for each derivation that has a bad step, in notebook order.

The tests check your checker on known steps and require `audit(NOTEBOOK)` to find exactly the two planted errors.

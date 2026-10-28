# Break it: Python-level loops

1. `row_norms_loop(X)`: the Euclidean norm of every row of `X`, computed with two nested Python loops, one multiply and add per element.
2. `row_norms_vector(X)`: the same with one vectorized expression.
3. `overhead_ratio(rows=200, cols=100, repeats=3)`: on `np.random.default_rng(0).normal(size=(rows, cols))`, the best-of-`repeats` time of the loop version divided by that of the vectorized one (use `time.perf_counter`).

Each loop iteration is one interpreted operation on one number, much as each eager PyTorch call is one kernel launch on one tensor. The ratio is the cost of overhead.

## Hints

1. Index with `X[i, j]` inside the loops.
2. `np.sqrt((X * X).sum(axis=1))` for the vectorized version.
3. Taking the best of several repeats removes noise from the measurement.

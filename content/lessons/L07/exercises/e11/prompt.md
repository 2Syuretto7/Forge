# Break it: Python-level loops

1. `row_norms_loop(X)`: the Euclidean norm of every row of `X`, computed with two nested Python loops, one multiply and add per element.
2. `row_norms_vector(X)`: the same with one vectorized expression.
3. `time_per_call(f, X, min_time=0.02)`: call `f(X)` 1, 2, 4, ... times in a row until one batch takes at least `min_time` seconds by `time.perf_counter`, and return that batch's time divided by its number of calls. Browser clocks tick in steps of up to a tenth of a millisecond, so a single fast call can measure as zero.
4. `overhead_ratio(rows=200, cols=100, repeats=3)`: on `np.random.default_rng(0).normal(size=(rows, cols))`, the best of `repeats` measurements of the loop version's time per call divided by that of the vectorized one.

Each loop iteration is one interpreted operation on one number, much as each eager PyTorch call is one kernel launch on one tensor. The ratio is the cost of overhead.

## Hints

1. Index with `X[i, j]` inside the loops.
2. `np.sqrt((X * X).sum(axis=1))` for the vectorized version.
3. Repeating a fast call until the total is long compared with the clock's step, then taking the best of several such measurements, removes both rounding and noise (this is what `timeit` does).

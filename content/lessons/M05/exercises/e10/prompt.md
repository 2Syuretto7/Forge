# Timing loops

Clocks are noisy, but a fit over several sizes recovers the exponent.

- `time_call(fn, n, min_time=0.02)`: the seconds per call of `fn(n)`, timing batches of calls that double in size until a batch takes at least `min_time` (as in M01's matrix timing).
- `fit_slope(xs, ys)`: least-squares slope (as in M04).
- `measured_exponent(fn, ns)`: the slope of $\log_{10}$ time against $\log_{10} n$ over the sizes `ns`.

The starter provides `single_loop(n)` and `double_loop(n)`, which do constant work $n$ and $n^2$ times. The tests measure both and expect exponents near 1 and 2, with a generous tolerance for noisy machines.

## Hints

1. `time.perf_counter()`.
2. Convert the sizes and times with `math.log10` before fitting.
3. Doubling batches keep short calls measurable on a coarse clock.

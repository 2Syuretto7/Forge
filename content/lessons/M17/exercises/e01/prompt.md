# Riemann sums and the trapezoid rule

For a vectorized function `f` (it accepts NumPy arrays):

- `riemann(f, a, b, n, where)`: the sum with `n` strips, sampling each strip at its `"left"` end, `"right"` end or `"mid"`dle.
- `trapezoid(f, a, b, n)`: the average of the left and right sums, equivalently weights $\frac h2(1, 2, 2, \dots, 2, 1)$.
- `observed_order(rule, f, a, b, exact, n)`: $\log_2$ of the error with `n` strips over the error with `2n`, where `rule(f, a, b, n)` is any of the rules.

The left and right sums have order 1; the midpoint and trapezoid rules order 2.

## Hints

1. `x = a + h * (np.arange(n) + offset)` with offset 0, 1 or 0.5.
2. One vectorized call per sum, no Python loop over strips.
3. `math.log2(err_n / err_2n)`.

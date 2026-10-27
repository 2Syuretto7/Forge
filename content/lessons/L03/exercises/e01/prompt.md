# Forward and central differences

Implement the two finite-difference formulas from Section 1 for a scalar function `f` of one variable.

- `forward_diff(f, x, h)` returns $\dfrac{f(x + h) - f(x)}{h}$.
- `central_diff(f, x, h)` returns $\dfrac{f(x + h) - f(x - h)}{2h}$.
- `error_ratio(f, df, x, h, method)` returns the ratio of the absolute error at step `h` to the absolute error at step `h/2`, where `df` is the exact derivative and `method` is `"forward"` or `"central"`.

For a first-order method the ratio is about 2; for a second-order method about 4, as long as rounding error is negligible.

## Hints

1. Both are one line each.
2. `error_ratio` calls the chosen method twice.
3. Use moderate steps such as `1e-2` when measuring orders; tiny steps bring rounding error into play.

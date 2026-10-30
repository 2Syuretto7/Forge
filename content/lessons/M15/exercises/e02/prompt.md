# Forward and central differences

- `forward_diff(f, x, h)`: $\dfrac{f(x + h) - f(x)}{h}$.
- `central_diff(f, x, h)`: $\dfrac{f(x + h) - f(x - h)}{2h}$.
- `error_ratio(f, df, x, h, method)`: the absolute error at step `h` divided by the absolute error at step `h/2`, where `df` is the exact derivative and `method` is `"forward"` or `"central"`.

For a first-order method the ratio is about 2; for a second-order method about 4, as long as rounding error is negligible.

## Hints

1. Both formulas are one line.
2. `error_ratio` calls the chosen method twice.
3. Use moderate steps such as `1e-2` when measuring orders; tiny steps bring rounding into play.

# The slope of the error law

If the error is $C n^{-p}$, then $\log_{10} \text{error} = \log_{10} C - p \log_{10} n$: a straight line on log-log axes with slope $-p$. Measure $p$.

- `fit_slope(xs, ys)`: the slope of the best straight line through the points, by the least-squares formula $\dfrac{\sum (x_i - \bar x)(y_i - \bar y)}{\sum (x_i - \bar x)^2}$ (M12 derives it; here, use it).
- `error_exponent(f, a, b, ns)`: measure the interpolation error for each $n$ in `ns` (use `np.interp` at 2,000 equally spaced points), and return $p$, minus the slope of $\log_{10}$ error against $\log_{10} n$.

## Hints

1. `xbar = sum(xs) / len(xs)`.
2. `np.log10(np.array(ns))`.
3. The tests expect $p$ close to 2 for smooth curves.

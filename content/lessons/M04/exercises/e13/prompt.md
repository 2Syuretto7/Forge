# The wrong order

A preprocessing pipeline is a composition, and it runs in order.

- `pipeline(steps)`: the machine that applies the functions in `steps` **left to right** (the first step acts first). Note this is the reverse of the $f \circ g$ reading order; pipelines in code usually read this way.
- `standardize(xs)`: subtract the mean and divide by the standard deviation $\sqrt{\frac{1}{n}\sum (x_i - \bar x)^2}$, returning a list.
- `clip(xs, lo, hi)`: replace each value below `lo` by `lo` and above `hi` by `hi`.
- `order_matters(xs, lo, hi)`: whether clipping then standardizing gives a different list from standardizing then clipping (compare with tolerance `1e-12`).

## Hints

1. `def machine(x): for f in steps: x = f(x); return x`.
2. Compute the mean, then the variance, then divide.
3. `pipeline([lambda v: clip(v, lo, hi), standardize])` is clip first.

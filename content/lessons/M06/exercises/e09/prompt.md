# A log-scale toolkit

- `log_ticks(lo, hi)`: the powers of ten $10^k$ with $\text{lo} \leq 10^k \leq \text{hi}$, as a list, for positive `lo` and `hi`.
- `fit_line(xs, ys)`: the least-squares line `(slope, intercept, r2)`, with $R^2$ as in M04's widget: the squared correlation, 1 for a perfect line.
- `straightness(xs, ys, xlog, ylog)`: the $R^2$ of a straight-line fit after taking $\log_{10}$ of the $x$ values if `xlog` and of the $y$ values if `ylog`.
- `best_axes(xs, ys)`: which of `"linear"`, `"semilog"` (log $y$ only) or `"loglog"` gives the largest straightness.

## Hints

1. Start from `k = math.ceil(math.log10(lo))` and go up while $10^k \leq$ `hi`.
2. $R^2 = \dfrac{S_{xy}^2}{S_{xx} S_{yy}}$ with $S$ the sums of products of deviations from the means.
3. Compare the three straightness values and return the name of the largest.

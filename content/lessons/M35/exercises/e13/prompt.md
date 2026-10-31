# Break it: a straight line through a floor

Fit e02's log-log line to data that have a floor, $L = E + Ax^{-\alpha}$ with $E = 1.7$. The line fits the data range with a high $R^2$, but its slope is too shallow and, extrapolated, it heads to zero as if the loss could fall without limit (Section 7). The fit with a floor predicts correctly.

- `fit_loglog(x, y)` as in e02.
- `fit_with_floor(x, y, theta0)`: Levenberg-Marquardt for $(E, A, \alpha)$, as in e05.
- `extrapolation_errors(x, y, x0, truth)`: the relative errors $\hat L(x_0)/L(x_0) - 1$ of the two fits at `x0`, as a tuple `(loglog, floor)`.

The tests use 30 points on $[1, 100]$ and find the log-log line at $x_0 = 10^5$ more than 10 percent below the truth (and below the floor $E$ itself), while the floor fit is within 1 percent.

## Hints

1. On log-log axes $E + Ax^{-\alpha}$ bends toward a horizontal line at $\log E$; a straight line through the bend has the wrong slope everywhere.
2. Residual plots in log space show the curvature that $R^2$ hides.
3. A pure power law is the special case $E = 0$; fitting $E$ costs one parameter and protects every extrapolation.

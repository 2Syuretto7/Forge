# Straight lines on log-log axes

The simplest fit of a power law is ordinary least squares on the logarithms: regress $\log y$ on $\log x$ and read off $-\alpha$ as the slope and $\log A$ as the intercept (Section 2). It is exact when the noise is multiplicative, $y = Ax^{-\alpha}e^{\varepsilon}$, because then the noise is additive in log space.

- `fit_loglog(x, y)`: `(A, alpha)` from `np.polyfit(log x, log y, 1)`.
- `loglog_r2(x, y)`: the $R^2$ of that fit in log space.
- `predict_loglog(A, alpha, x)`.

The tests recover a power law from noisy multiplicative data, and show that a high $R^2$ alone proves little: data with a loss floor, $y = 0.5 + 2x^{-0.5}$ on $[1, 100]$, also give $R^2$ above $0.98$ on log-log axes, while the fitted exponent is $0.28$ instead of $0.5$.

## Hints

1. `np.polyfit(u, v, 1)` returns `[slope, intercept]`.
2. $R^2 = 1 - \text{residual sum of squares}/\text{total sum of squares}$.
3. A floor bends the log-log curve, but gently over two decades: curvature hides inside a good $R^2$.

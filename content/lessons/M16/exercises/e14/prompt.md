# Gradient descent past 2/L

- `gd_quadratic(L, eta, x0, steps)`: iterates of gradient descent on $\frac{L}{2}x^2$.
- `growth(L, eta)`: the factor $|1 - \eta L|$; above 1 the iterates grow.
- `first_blowup(f, df, x0, eta, limit=1e6)`: the first step at which $|x|$ exceeds `limit` (or `None` within 1,000 steps).
- `largest_safe_eta(df, x0, etas, steps=200)`: the largest step in the list `etas` for which gradient descent from `x0` ends within $10^{-6}$ of 0 after `steps` steps.

On a non-quadratic function the threshold depends on where you start: for $f(x) = x^2 + x^4/4$ the curvature at 0 is 2, so steps just below $2/2 = 1$ converge from a small start (slowly: at $\eta = 0.99$ the factor is 0.98), while from $x_0 = 1.5$, where the curvature is $2 + 3x^2 = 8.75$, a step of 0.5 already blows up.

## Hints

1. Reuse your iteration from e07.
2. On the quadratic the $k$-th iterate is $(1 - \eta L)^k x_0$ exactly.
3. Scan `etas` in increasing order and keep the last that works.

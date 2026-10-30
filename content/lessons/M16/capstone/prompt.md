# Capstone: a one-dimensional optimizer suite

The starter's `PROBLEMS` lists test functions as `(name, f, df, d2f, x0, xstar)`, with `xstar` the minimizer.

1. `gd_min(df, x0, eta, steps=300)`, `secant_min(df, x0, x1, steps=60)` (the secant method applied to $f'$) and `newton_min(df, d2f, x0, steps=30)`: each returns the list of iterates, stopping early once a step is below $10^{-15}\max(1, |x|)$.
2. `measured_order(errs)`: the median of the order estimates $\ln(e_{k+1}/e_k)/\ln(e_k/e_{k-1})$ over consecutive errors between $10^{-13}$ and $0.3$ (Newton reaches full precision in so few steps that a narrower window can leave fewer than three usable errors).
3. `measured_rate(errs)`: the median ratio $e_{k+1}/e_k$ over the same window.
4. `report()`: for each problem, a dictionary with `"name"`, `"gd_order"`, `"gd_rate"`, `"gd_predicted_rate"` ($|1 - \eta f''(x^\ast)|$, using $\eta = 0.5 / f''(x^\ast)$, so the prediction is 0.5), `"secant_order"` and `"newton_order"`.

None of the problems is symmetric about its minimizer: at a symmetric minimum the third derivative vanishes and Newton converges even faster than quadratically, too fast to measure. The tests require, for every problem, gradient descent's order within 10 percent of 1 and its rate within 10 percent of the prediction, the secant order within 10 percent of 1.618, and Newton's order within 10 percent of 2.

# The secant method

- `secant(f, x0, x1, tol=1e-14, max_iter=100)`: replace the derivative in Newton's step by the slope through the last two points, $x_{k+1} = x_k - f(x_k)\frac{x_k - x_{k-1}}{f(x_k) - f(x_{k-1})}$. Stop when the step is below `tol` times $\max(1, |x|)$ or when $f(x_k) = f(x_{k-1})$. Return `(x, history)`.
- `order_estimates(errors)`: for consecutive errors, $p_k = \ln(e_{k+1}/e_k) / \ln(e_k/e_{k-1})$, using only errors between $10^{-13}$ and $10^{-1}$.

The secant method reuses the previous evaluation, so it needs one new value of $f$ per step: its order, $(1 + \sqrt 5)/2 \approx 1.618$, buys more per evaluation than Newton's 2 with two evaluations.

## Hints

1. Keep the last two points and their values.
2. Filter the error list before forming ratios.
3. The estimates scatter around 1.6 because only a few steps fall in the usable range.

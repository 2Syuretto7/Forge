# Integrating a singularity naively

$\int_0^1 x^{-1/2}\,dx = 2$, with an infinite integrand at 0.

- `midpoint_errors(ns)`: the errors of the midpoint rule with each number of strips in `ns` (the midpoint rule never evaluates at 0).
- `fitted_order(ns, errs)`: the slope of $-\log(\text{error})$ against $\log n$ (least squares, `np.polyfit`): the order of convergence.
- `after_substitution(n)`: the error of Simpson's rule with `n` strips on the substituted integral $\int_0^1 2t \cdot (t^2)^{-1/2}\,dt$, with the integrand written as the constant 2 it simplifies to.

The fitted order is about $1/2$ before the substitution; after it, the integral is computed exactly.

## Hints

1. Midpoints: `(np.arange(n) + 0.5) / n`.
2. `np.polyfit(np.log(ns), -np.log(errs), 1)[0]`.
3. $2t \cdot t^{-1} = 2$.

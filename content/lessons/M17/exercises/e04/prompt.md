# Accumulation and its derivative

- `cumulative(f, a, b, n)`: the trapezoid-rule running integral: arrays `(x, F)` with `x` the `n + 1` grid points and `F[k]` the integral from `a` to `x[k]`.
- `derivative_of_cumulative(x, F)`: central differences $(F_{k+1} - F_{k-1}) / (x_{k+1} - x_{k-1})$ at the interior points.

The tests run a **gradient check** of the fundamental theorem: the derivative of the accumulated area equals the integrand.

## Hints

1. `np.cumsum` of the trapezoid areas $\frac h2(y_k + y_{k+1})$, with a leading 0.
2. Interior points are `x[1:-1]`.
3. Both steps have error of order $h^2$.

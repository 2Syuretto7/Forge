# 100,000 cube roots at once

- `newton_cbrt_vec(a, iters)`: for an array `a` of positive numbers, run `iters` vectorized Newton steps on $x^3 - a$ from $x_0 = a$ (or 1 where $a < 1$), and return the array.
- `steps_to_converge(a, method, tol=1e-15)`: the number of vectorized steps until every element has relative error below `tol` against `np.cbrt(a)`, for `"newton"` or `"bisect"` (bisection on the bracket $[0, \max(1, a)]$, all brackets halved together).

The tests solve 100,000 problems with values from $10^{-3}$ to $10^{3}$: Newton needs about 20 steps (the start $x_0 = a$ is poor for large $a$: early steps only shrink $x$ by about a third), bisection about 60.

## Hints

1. Newton step for $x^3 - a$: $x - (x^3 - a)/(3x^2) = \frac{2x}{3} + \frac{a}{3x^2}$.
2. For bisection keep arrays `lo` and `hi` and update them with `np.where`.
3. Stop counting when `np.all(rel < tol)`.

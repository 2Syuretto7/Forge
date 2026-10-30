# A jump spoils the order

The step $H(x) = 1$ for $x > 1/3$, 0 otherwise, has $\int_0^1 H = 2/3$.

- `simpson_step_errors(ns)`: Simpson's errors for $H$ with each even `n` in `ns`.
- `fitted_order(ns, errs)`: as in e13.
- `split_at_jump(n)`: the error when the integral is split at $1/3$ and Simpson's rule is applied to each piece separately with `n` strips each.

With the jump inside a strip, Simpson's order drops from 4 to about 1; splitting at the jump restores exactness (each piece is constant).

## Hints

1. A step function: `(x > 1/3).astype(float)`.
2. Use values of `n` that are not multiples of 3, so the jump never falls on a grid point.
3. Each piece of the split integral is a constant function.

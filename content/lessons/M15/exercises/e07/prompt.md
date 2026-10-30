# Corners

- `one_sided(f, a, h=1e-7)`: `(left, right)`, the slopes $(f(a) - f(a - h))/h$ and $(f(a + h) - f(a))/h$.
- `has_corner(f, a, h=1e-7, tol=1e-4)`: whether the two one-sided slopes differ by more than `tol`.
- `relu_grad(x)`: the derivative of the ReLU with the convention used by frameworks: 1 for $x > 0$, 0 for $x \leq 0$.
- `abs_subgradients(x)`: the interval `(lo, hi)` of slopes of lines touching $|x|$ at `x` from below: $(-1, 1)$ at 0, otherwise the derivative twice.

The tests check that smooth functions pass `has_corner` as cornerless and that their one-sided slopes agree with the derivative (a **gradient check**).

## Hints

1. Two difference quotients.
2. Compare `abs(right - left)` with `tol`.
3. `math.copysign(1, x)` for $x \neq 0$.

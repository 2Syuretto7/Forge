# The best linear approximation

- `tangent(f, df, a)`: the function $x \mapsto f(a) + f'(a)(x - a)$.
- `linear_error(f, df, a, h)`: $|f(a + h) - f(a) - f'(a)h|$, the error of the tangent at distance $h$.
- `error_order(f, df, a, h)`: `linear_error` at `h` divided by `linear_error` at `h/2`.

For a differentiable function the ratio is about 4: the error shrinks like $h^2$, faster than $h$. For $|x|$ at 0 with any slope you choose, the ratio is 2: no line approximates a corner better than linearly.

## Hints

1. Return a closure.
2. The tests use $h = 10^{-2}$.
3. Try `error_order(abs, lambda x: 0.3, 0.0, 1e-2)`.

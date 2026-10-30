# Newton's method

- `newton(f, df, x0, tol=1e-14, max_iter=50)`: iterate $x \leftarrow x - f(x)/f'(x)$ until the step is smaller than `tol` times $\max(1, |x|)$; return `(x, history)` with `history` the list of all iterates, `x0` included. Raise `ValueError` if `df` returns 0.
- `newton_sqrt(a)`: $\sqrt a$ for $a > 0$ by `newton` on $x^2 - a$ from $x_0 = a$ (or 1 if $a < 1$).

The tests check quadratic convergence on $\sqrt 2$: the ratio $e_{k+1}/e_k^2$ settles near $1/(2\sqrt 2)$.

## Hints

1. Append to `history` after each step.
2. $f'(x) = 2x$ for $x^2 - a$.
3. Errors: `abs(x - math.sqrt(2))` for each iterate.

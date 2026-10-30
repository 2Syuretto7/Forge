# Newton for minimization finds a maximum

$f(x) = x^4/4 - x^2$ has minima at $\pm\sqrt 2$ and a maximum at 0.

- `newton_min(df, d2f, x0, steps=50)`: plain Newton on $f'$: $x \leftarrow x - f'(x)/f''(x)$.
- `safe_newton_min(df, d2f, x0, eta=0.1, steps=200)`: use the Newton step only where $f''(x) > 0$; elsewhere take a gradient step $x - \eta f'(x)$.

From $x_0 = 0.3$, where $f'' < 0$, plain Newton converges to the maximum at 0: it only looks for a critical point. The safe version reaches a minimum. The tests include a **gradient check** that your $f'$ and $f''$ formulas match central differences.

## Hints

1. $f'(x) = x^3 - 2x$ and $f''(x) = 3x^2 - 2$.
2. The safe version's first steps are gradient steps away from 0.
3. Check $f''$ at the result to tell a minimum from a maximum.

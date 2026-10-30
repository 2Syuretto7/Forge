# Second-order Taylor and the descent lemma

- `taylor2(f0, g, H, h)`: the second-order prediction $f_0 + g \cdot h + \frac12 h^\top H h$.
- `descent_bound(gnorm2, L, eta)`: the guaranteed decrease $\eta\|g\|^2 - \frac12 L\eta^2\|g\|^2$ for curvature at most $L$.
- `gd_step_decrease(f, grad, x, eta)`: the actual decrease $f(x) - f(x - \eta\nabla f(x))$.

For a quadratic the bound is exact when the gradient lies along the top eigenvector; elsewhere the decrease is larger. The tests check both (a **gradient check** of the bound), and that the second-order Taylor error of a smooth function shrinks like $\|h\|^3$.

## Hints

1. `f0 + g @ h + 0.5 * h @ H @ h`.
2. `gnorm2` is $\|g\|^2$.
3. Halving $h$ divides a third-order error by about 8.

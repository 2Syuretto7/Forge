# Taylor's theorem and the descent lemma, measured

Check Section 7 numerically.

- `taylor2(f0, g, H, h)`: the second-order prediction $f_0 + g^\top h + \tfrac12 h^\top H h$.
- `descent_bound(gnorm2, L, eta)`: the guaranteed decrease $\eta\|g\|^2 - \tfrac12 L\eta^2\|g\|^2$ for a function whose curvature is at most $L$.
- `gd_step_decrease(f, grad, x, eta)`: the actual decrease $f(x) - f(x - \eta \nabla f(x))$.

For a quadratic, the bound is exact when the gradient points along the top eigenvector; for other directions the actual decrease is larger. The tests check both, and that the second-order Taylor error of a smooth non-quadratic function shrinks like $\|h\|^3$.

## Hints

1. `f0 + g @ h + 0.5 * h @ H @ h`.
2. The bound is a scalar formula; `gnorm2` is $\|g\|^2$.
3. Halving $h$ should divide a third-order error by about 8.

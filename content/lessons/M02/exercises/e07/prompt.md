# Inequalities and absolute values

Write `solve_inequality(a, b, c)` for $a x + b < c$. Return:

- `("<", bound)` when the solutions are $x <$ bound;
- `(">", bound)` when they are $x >$ bound (this happens when $a < 0$: dividing by a negative number flips the inequality);
- `"all"` when $a = 0$ and the inequality $b < c$ is true, and `None` when $a = 0$ and it is false.

Then `abs_interval(center, radius)` for $|x - \text{center}| < \text{radius}$ returns the open interval `(lo, hi)`, or `None` if the radius is not positive. And `satisfies(a, b, c, x)` returns whether a particular `x` satisfies $a x + b < c$, so the tests can check your answers point by point.

## Hints

1. Subtract $b$: $a x < c - b$. Then divide by $a$, flipping the direction when $a < 0$.
2. $|x - m| < r$ means $m - r < x < m + r$.
3. `satisfies` is one comparison.

# The forgotten absolute value

$X$ uniform on $(0, 1]$ and $Y = 1/X$, a decreasing map onto $[1, \infty)$.

- `signed_density(y)`: $p_X(g^{-1}(y)) \cdot (g^{-1})'(y)$ without the absolute value.
- `density(y)`: with it: $1/y^2$.
- `prob_greater(t)`: $P(Y > t) = P(X < 1/t) = 1/t$, from the density by integrating it, or directly.

The signed version is negative everywhere: a decreasing map reverses orientation, and the formula needs the size of the stretch, not its direction.

## Hints

1. $g^{-1}(y) = 1/y$ and its derivative is $-1/y^2$.
2. `abs`.
3. Check: $\int_t^\infty y^{-2}\,dy = 1/t$.

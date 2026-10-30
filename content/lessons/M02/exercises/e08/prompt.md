# The quadratic formula

Write `solve_quadratic(a, b, c)` for $a x^2 + b x + c = 0$ with $a \neq 0$. Return a sorted list of the distinct real solutions: two numbers when the discriminant $D = b^2 - 4ac$ is positive, one when it is zero, and an empty list when it is negative. Raise `ValueError` when $a = 0$ (that equation is linear, not quadratic).

Also write `discriminant(a, b, c)`.

The tests check an **invariant**: every root you return makes $a x^2 + b x + c$ tiny compared with the size of its terms, for thousands of random quadratics.

## Hints

1. `math.sqrt(D)` for $D \geq 0$.
2. `sorted([r1, r2])`; when $D = 0$ return `[-b / (2 * a)]`.
3. The size of the terms at a root $r$ is about `abs(a * r * r) + abs(b * r) + abs(c)`.

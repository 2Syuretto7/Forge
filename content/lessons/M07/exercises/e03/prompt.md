# Rotation by trigonometry

- `rotate(p, theta)`: the point `p = (x, y)` turned by `theta` about the origin, by the formula of Section 3.
- `rotate_about(p, center, theta)`: turned about another point: shift so the center is at the origin, rotate, shift back (a composition, as in M04).
- `rotation_matrix(theta)`: the 2 by 2 matrix as a list of rows `[[c, -s], [s, c]]`, and `apply(M, p)`, which multiplies a matrix (list of rows) by a point.

## Hints

1. `(x * c - y * s, x * s + y * c)` with `c, s = math.cos(theta), math.sin(theta)`.
2. Subtract the center, rotate, add the center.
3. `apply` computes `(M[0][0] * x + M[0][1] * y, M[1][0] * x + M[1][1] * y)`.

# Projection onto a line

- `project(b, a)`: the projection of `b` onto the line through `a` (nonzero), $\frac{a \cdot b}{a \cdot a}\,a$, as a NumPy array.
- `residual(b, a)`: `b - project(b, a)`.
- `component(b, a)`: the signed length of the projection, $\frac{a \cdot b}{\|a\|}$.

The tests check an **invariant**: the residual is perpendicular to `a`, projecting twice changes nothing, and Pythagoras holds: $\|b\|^2 = \|p\|^2 + \|b - p\|^2$.

## Hints

1. `(a @ b) / (a @ a) * a`.
2. Use `np.dot` or `@` freely now.
3. `component` is the dot product with the unit vector along `a`.

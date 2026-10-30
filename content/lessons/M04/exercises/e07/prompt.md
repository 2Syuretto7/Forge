# Transformations

Each transformation of a graph is a composition with an affine machine (Section 5).

- `shift(f, h, k)`: the machine $x \mapsto f(x - h) + k$ (right by $h$, up by $k$).
- `stretch(f, a, b)`: the machine $x \mapsto b\, f(x / a)$ (horizontally by $a$, vertically by $b$).
- `reflect_y(f)`: $x \mapsto f(-x)$; `reflect_x(f)`: $x \mapsto -f(x)$.
- `vertex_after_shift(h, k)`: the lowest point of $x^2$ shifted right by $h$ and up by $k$, as a pair.

The tests check an **invariant**: shifting twice is one shift by the sums, `shift(shift(f, h1, k1), h2, k2)` equals `shift(f, h1 + h2, k1 + k2)` at random points, for several functions.

## Hints

1. `return lambda x: f(x - h) + k`.
2. `return lambda x: b * f(x / a)`.
3. The vertex of $x^2$ is at $(0, 0)$; a shift moves it to $(h, k)$.

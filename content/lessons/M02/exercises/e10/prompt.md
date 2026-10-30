# Solve ten thousand systems at once

NumPy arrays let one line of code act on every element. Write:

- `determinants(A)` for an array `A` of shape `(n, 2, 2)`: the array of the $n$ determinants $a_{00} a_{11} - a_{01} a_{10}$.
- `solve_many(A, rhs)` for `A` of shape `(n, 2, 2)` and `rhs` of shape `(n, 2)`: the array of shape `(n, 2)` of solutions, by the elimination formula applied to whole arrays. No Python loop over the $n$ systems.

`A[:, 0, 0]` is the array of every system's top-left entry. Arithmetic on arrays happens elementwise, and `np.stack([x, y], axis=1)` assembles two length-$n$ arrays into an `(n, 2)` array.

## Hints

1. `a, b, c, d = A[:, 0, 0], A[:, 0, 1], A[:, 1, 0], A[:, 1, 1]`.
2. `p, q = rhs[:, 0], rhs[:, 1]`.
3. The tests compare with `np.linalg.solve`, which does the same job.

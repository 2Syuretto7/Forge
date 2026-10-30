# A 2D graphics pipeline

Points are stored as rows of an `(N, 2)` array.

- `apply(M, P)`: the points after the 2 by 2 matrix `M` (each row $p$ becomes $Mp$; with rows, that is `P @ M.T`).
- `compose(*Ms)`: one matrix for "apply `Ms[0]`, then `Ms[1]`, ...". The first one applied must stand **rightmost** in the product.
- `to_h(P)` and `from_h(H)`: homogeneous coordinates, appending a column of ones and dropping it. A translation is then a 3 by 3 matrix, `translate(tx, ty)`, and every 2 by 2 `M` becomes `lift(M)`, 3 by 3 with `M` in the corner.
- `rotate_about(theta, c)`: the 3 by 3 matrix that rotates by `theta` about the point `c`: move `c` to the origin, rotate, move back.

## Hints

1. `compose` multiplies in reverse order: `Ms[-1] @ ... @ Ms[0]`.
2. `np.hstack([P, np.ones((len(P), 1))])`.
3. `translate(*c) @ lift(R) @ translate(-c[0], -c[1])`.

# Coordinates in an orthonormal basis

For `Q` with orthonormal columns (shape `(m, n)`):

- `coefficients(Q, b)`: $Q^\top b$, the coordinates of the projection.
- `project_orthonormal(Q, b)`: $QQ^\top b$.
- `energy_split(Q, b)`: `(inside, outside)` with `inside` $= \|Q^\top b\|^2$ and `outside` $= \|b - QQ^\top b\|^2$.

The tests check an **invariant** for random orthonormal bases: `inside + outside` equals $\|b\|^2$ (Pythagoras), and the projection's length equals the length of its coordinate vector.

## Hints

1. No solving is needed when $Q^\top Q = I$.
2. A random orthonormal `Q`: `np.linalg.qr(rng.normal(size=(m, n)))[0]`.
3. `float(c @ c)` for a squared length.

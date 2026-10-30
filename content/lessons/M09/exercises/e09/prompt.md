# The Gram matrix

The **Gram matrix** of vectors $x_1, \dots, x_n$ is the table of all their dot products, $G_{ij} = x_i \cdot x_j$, which is `X @ X.T` for the rows of `X`.

- `gram(X)`: the Gram matrix.
- `quadratic_form(G, z)`: $z^\top G z = \sum_{i,j} z_i G_{ij} z_j$.
- `as_squared_length(X, z)`: $\|\sum_i z_i x_i\|^2$, the squared length of the combination of rows with weights `z`.

These two are equal (expand the length with linearity), so $z^\top G z \geq 0$ for every `z`. The tests check that **invariant** on many random matrices and weights.

## Hints

1. `X @ X.T`.
2. `z @ G @ z`.
3. `v = z @ X`, then `v @ v`.

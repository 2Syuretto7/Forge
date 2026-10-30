# Projections onto lines and subspaces

- `project_onto_line(b, a)`: the point of the line through `a` nearest to `b`.
- `projection_matrix(A)`: for `A` of shape `(m, n)` with independent columns, the `(m, m)` matrix $P = A(A^\top A)^{-1}A^\top$. Use `np.linalg.solve` rather than forming an inverse.
- `project(b, A)`: the projection of `b` onto the column space of `A`, by solving the normal equations and returning $A\hat x$.

The tests check an **invariant** on random matrices: $P^\top = P$, $P^2 = P$, and the residual $b - Pb$ is perpendicular to every column.

## Hints

1. On a line: $p = \dfrac{a \cdot b}{a \cdot a} a$.
2. `np.linalg.solve(A.T @ A, A.T)` computes $(A^\top A)^{-1} A^\top$ without an inverse.
3. `project` need not build $P$: solve $A^\top A x = A^\top b$ and return `A @ x`.

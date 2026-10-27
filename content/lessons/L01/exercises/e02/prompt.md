# Projections onto lines and subspaces

Implement orthogonal projection, following Sections 2 and 3 of the derivation.

- `project_onto_line(b, a)`: the closest point to `b` on the line spanned by `a` (both shape `(m,)`).
- `projection_matrix(A)`: for `A` of shape `(m, n)` with independent columns, return the `(m, m)` matrix $P = A(A^\top A)^{-1}A^\top$. Use `np.linalg.solve` rather than forming an explicit inverse.
- `project(b, A)`: the projection of `b` onto the column space of `A`, shape `(m,)`.

The tests check the defining properties: $P^\top = P$, $P^2 = P$, and that the residual $b - Pb$ is orthogonal to every column of $A$.

## Hints

1. On a line: $p = \dfrac{a^\top b}{a^\top a} a$.
2. `np.linalg.solve(A.T @ A, A.T)` computes $(A^\top A)^{-1} A^\top$ without an explicit inverse.
3. `project(b, A)` can reuse `projection_matrix`, but solving $A^\top A x = A^\top b$ and returning $Ax$ is cheaper.

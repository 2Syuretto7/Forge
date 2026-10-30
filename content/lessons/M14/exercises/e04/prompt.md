# The pseudo-inverse

- `pinv(A, rtol=1e-12)`: $V\Sigma^+U^\top$ from `np.linalg.svd(A, full_matrices=False)`, treating singular values at most `rtol` $\cdot \sigma_1$ as zero.
- `min_norm_solution(A, b)`: $A^+ b$.

The tests check an **invariant** on random matrices of every shape and rank, the four Penrose conditions that characterize $A^+$: $AA^+A = A$, $A^+AA^+ = A^+$, and both $AA^+$ and $A^+A$ symmetric. They also check that for one equation in several unknowns the solution is the shortest one.

## Hints

1. `s_inv = np.where(s > rtol * s[0], 1 / s, 0)`, guarding the zero matrix.
2. `Vt.T @ np.diag(s_inv) @ U.T`, or scale the columns of `Vt.T` directly.
3. The shortest solution has no component in the null space of $A$.

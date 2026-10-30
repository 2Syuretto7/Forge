# Solving and determinants from LU

Given the factors of $PA = LU$ (the starter provides a working `lu`):

- `lu_solve(P, L, U, b)`: solve $Ax = b$: $Ly = Pb$ by forward substitution, then $Ux = y$.
- `det_from_lu(P, U)`: $\det A = \det(P)^{-1} \prod_i U_{ii}$, where $\det P$ is $+1$ or $-1$ for an even or odd number of swaps.
- `solve_many(A, B)`: factor once and solve for every column of `B` (shape `(n, k)`); return `X` of shape `(n, k)`.

## Hints

1. `P @ b` reorders the right-hand side the way the rows were swapped.
2. The sign of a permutation matrix is its determinant; count the swaps needed to sort the row order, or compute `np.linalg.det(P)` rounded, which is fine here.
3. Stack the column solutions with `np.column_stack`.

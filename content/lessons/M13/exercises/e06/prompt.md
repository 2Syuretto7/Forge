# Positive definiteness and Cholesky

- `classify_form(S, tol=1e-12)`: from the eigenvalues of symmetric `S`, one of `"positive definite"`, `"positive semidefinite"`, `"negative definite"`, `"negative semidefinite"`, `"indefinite"` (an eigenvalue with absolute value at most `tol` counts as zero).
- `cholesky(S)`: the lower triangular `L` with $LL^\top = S$, column by column: $L_{jj} = \sqrt{S_{jj} - \sum_{k<j} L_{jk}^2}$ and $L_{ij} = (S_{ij} - \sum_{k<j} L_{ik}L_{jk}) / L_{jj}$ below it. Raise `ValueError` when the number under a square root is not positive.
- `is_pd(S)`: whether `cholesky` succeeds.

## Hints

1. `np.linalg.eigvalsh(S)` for the classification.
2. `L[j, :j] @ L[j, :j]` is the sum of squares in the diagonal formula.
3. Cholesky costs about $n^3/3$ operations, a third of an eigen-decomposition's work, which is why it is the standard test.

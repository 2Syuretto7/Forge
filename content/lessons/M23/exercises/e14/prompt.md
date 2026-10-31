# Break it: a correlation matrix that cannot exist

Estimate each correlation from a different subset of the data, as happens with missing values, and the assembled matrix may not be positive semidefinite: no random vector has those correlations. Cholesky fails, and a variance computed from it can come out negative.

- `is_psd(C, tol=1e-10)`: whether the smallest eigenvalue is at least `-tol`.
- `negative_variance_direction(C)`: a unit vector $a$ with the most negative $a^\top C a$, the eigenvector of the smallest eigenvalue.
- `nearest_correlation(C, eps=1e-6)`: clip the eigenvalues of $C$ at `eps`, rebuild the matrix, and rescale it so the diagonal is exactly 1.

## Hints

1. `w, V = np.linalg.eigh(C)`; `V[:, 0]` belongs to the smallest eigenvalue.
2. Rebuild with `(V * np.maximum(w, eps)) @ V.T`.
3. Rescale with `D = 1 / np.sqrt(np.diag(M))` and `M * np.outer(D, D)`.

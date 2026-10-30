# Projection that survives dependent columns

- `column_space_basis(A, rtol=1e-10)`: the left singular vectors for singular values above `rtol` $\cdot\sigma_1$, an orthonormal basis of the column space, shape `(m, r)`.
- `project_svd(b, A)`: the projection of `b` onto the column space, $U_r U_r^\top b$.

M12's formula $A(A^\top A)^{-1}A^\top b$ needs independent columns; this one does not. The tests compare the two on independent columns and then add a column that is a combination of the others.

## Hints

1. `U, s, Vt = np.linalg.svd(A, full_matrices=False)`.
2. Count `r = np.sum(s > rtol * s[0])`.
3. The projection of a vector already in the column space is itself.

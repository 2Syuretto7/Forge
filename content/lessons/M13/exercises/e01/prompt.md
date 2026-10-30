# Eigenpairs of small matrices

- `is_eigenpair(A, lam, v, tol=1e-9)`: whether `v` is nonzero and $\|Av - \lambda v\| \leq$ `tol` $\cdot \max(1, \|A\|_F \|v\|)$.
- `char_poly2(A)`: the coefficients `(1, -trace, det)` of $\lambda^2 - (\operatorname{tr} A)\lambda + \det A$ for a 2 by 2 matrix.
- `eig2_real(A)`: its two eigenvalues by the quadratic formula, larger first, as floats; raise `ValueError` when they are complex.

The tests check an **invariant** on random symmetric 2 by 2 matrices: the eigenvalues add to the trace and multiply to the determinant, and NumPy's eigenvectors pass `is_eigenpair` with them.

## Hints

1. `np.linalg.norm(A @ v - lam * v)`.
2. The discriminant is $\operatorname{tr}^2 - 4\det$.
3. `np.linalg.eigh` returns eigenvalues in increasing order and eigenvectors as columns.

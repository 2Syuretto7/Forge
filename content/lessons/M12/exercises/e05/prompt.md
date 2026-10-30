# Least squares two ways

For tall `A` with independent columns:

- `lstsq_normal(A, b)`: solve $A^\top A x = A^\top b$ with `np.linalg.solve`.
- `lstsq_qr(A, b)`: factor with `np.linalg.qr` (Householder reflections) and solve $Rx = Q^\top b$.
- `residual_report(A, b, x)`: a dictionary with `"residual_norm"`, $\|Ax - b\|$, and `"max_orthogonality"`, $\max_j |a_j \cdot r|$ with $r = b - Ax$, both Python floats.

## Hints

1. `np.linalg.qr(A)` returns the reduced `Q` `(m, n)` and `R` `(n, n)`.
2. `np.max(np.abs(A.T @ r))`.
3. On well-conditioned problems both methods agree to many digits; Movement 4 shows where they part.

# Least squares two ways

Solve $\min_x \|Ax - b\|^2$ for tall `A` `(m, n)` with independent columns and `b` `(m,)`.

- `lstsq_normal(A, b)`: solve the normal equations $A^\top A x = A^\top b$ with `np.linalg.solve`.
- `lstsq_qr(A, b)`: factor $A = QR$ with `np.linalg.qr` (reduced mode, the default) and solve $Rx = Q^\top b$. You may use `np.linalg.solve` for the triangular system here.
- `residual_report(A, b, x)`: return a dict with keys `"residual_norm"` ($\|Ax - b\|$) and `"max_orthogonality"` ($\max_j |a_j^\top r|$ where $r = b - Ax$).

On well-conditioned problems both solvers agree to many digits. Movement 5 shows where they part ways.

## Hints

1. `np.linalg.qr(A)` returns `Q` of shape `(m, n)` and `R` of shape `(n, n)`.
2. `np.max(np.abs(A.T @ r))` is the orthogonality measure.
3. Convert the values in the report to Python floats.

# Ridge regression without forming the matrix

Ridge regression solves $(X^\top X + \lambda I)w = X^\top y$. Forming $X^\top X$ costs $2Nd^2$ flops and squares the condition number (M26); conjugate gradient needs only products $v \mapsto X^\top(Xv) + \lambda v$, two passes over $X$ each (Section 3). The matrix is symmetric positive definite, so CG applies, and its condition number is at most $(\sigma_1^2 + \lambda)/\lambda$: the penalty that regularizes the model also speeds up the solver.

- `ridge_loss(w, X, y, lam)`: $\frac12\lVert Xw - y\rVert^2 + \frac\lambda2\lVert w\rVert^2$, and `grad_ridge_loss(w, X, y, lam)`: $X^\top(Xw - y) + \lambda w$.
- `ridge_cg(X, y, lam, tol=1e-10)`: CG on the normal equations with matrix-free products; returns `(w, n_matvecs)` counting products with $X^\top X + \lambda I$.
- `ridge_direct(X, y, lam)`: `np.linalg.solve` on the formed matrix.

The tests run a **gradient check**, solve a $5{,}000 \times 150$ problem both ways, and find CG needing fewer products for larger $\lambda$.

## Hints

1. The gradient of the loss is the negative residual of the normal equations, so CG is driving the gradient to zero.
2. Write the product as `X.T @ (X @ v) + lam * v`, never `(X.T @ X) @ v`.
3. Count one product per CG iteration.

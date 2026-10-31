# Conjugate gradient

For a symmetric positive definite $A$, solving $Ax = b$ is minimizing $f(x) = \frac12x^\top Ax - b^\top x$, whose gradient is $Ax - b$, the negative residual (Section 3). Conjugate gradient moves along directions that are $A$-orthogonal, $p_i^\top Ap_j = 0$, so no step undoes an earlier one, and each needs one matrix-vector product:

$$
\alpha_k = \frac{r_k^\top r_k}{p_k^\top Ap_k},\quad x_{k+1} = x_k + \alpha_kp_k,\quad r_{k+1} = r_k - \alpha_kAp_k,\quad p_{k+1} = r_{k+1} + \frac{r_{k+1}^\top r_{k+1}}{r_k^\top r_k}\,p_k .
$$

- `quadratic(A, b, x)` and `grad_quadratic(A, b, x)`.
- `cg(matvec, b, tol=1e-10, max_iter=None)`: start from $x_0 = 0$, $r_0 = p_0 = b$; stop when $\lVert r\rVert \le$ `tol` $\cdot\lVert b\rVert$ or after `max_iter` iterations (default $10n$). Return `(x, residual_norms, directions)`, where `residual_norms` starts with $\lVert b\rVert$ and `directions` lists the search directions used.

The tests run a **gradient check**, solve a 200-dimensional system, and confirm that the directions are $A$-orthogonal.

## Hints

1. `matvec` is a function, so the same code works for a matrix that is never stored.
2. Compute `A @ p` once per iteration and reuse it.
3. In exact arithmetic CG finishes in at most $n$ steps; in floating point the directions slowly lose conjugacy, which is why the stopping rule tests the residual.

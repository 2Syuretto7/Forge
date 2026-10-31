# Break it: conjugate gradient on the wrong matrix

Every step of CG's derivation used symmetry and positive definiteness: $f(x) = \frac12x^\top Ax - b^\top x$ has gradient $Ax - b$ only for symmetric $A$, and it has a minimum only when $A$ is positive definite (Section 3). Hand CG a non-symmetric matrix and it neither minimizes anything nor stops.

- `cg_residuals(A, b, iters)`: the relative residual norms $\lVert r_k\rVert/\lVert b\rVert$ of plain CG for `iters` iterations, run without a stopping test.
- `cgnr(A, b, tol=1e-10, max_iter=5000)`: CG on the normal equations $A^\top Ax = A^\top b$, which are symmetric positive definite for any invertible $A$, with products $v \mapsto A^\top(Av)$. Returns `(x, iterations)`.
- `make_nonsymmetric(n, rng)` is provided.

The tests find plain CG's residual still above $10^{-2}$ after $3n$ iterations, while CGNR solves the same system to $10^{-8}$.

## Hints

1. Plain CG on a non-symmetric matrix builds directions that are not conjugate, so the step lengths are wrong; the residual wanders.
2. CGNR squares the condition number, so it is slower than CG on a symmetric problem of the same conditioning; GMRES and BiCGSTAB are the usual alternatives.
3. Stop iterating, rather than divide by zero, if $p^\top Ap$ becomes exactly 0.

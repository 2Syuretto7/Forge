# The minimum-norm solution, by Lagrange

An underdetermined system $Ax = b$ ($m < n$ equations) has infinitely many solutions. The one closest to the origin minimizes $\frac12\lVert x\rVert^2$ subject to $Ax = b$. The Lagrangian $\frac12\lVert x\rVert^2 + \lambda^\top(Ax - b)$ is stationary at $x = -A^\top\lambda$, and the constraint then gives $\lambda = -(AA^\top)^{-1}b$ (Section 1).

- `min_norm(A, b)`: return `(x, lam)`.
- `check_stationarity(A, x, lam)`: the norm of $x + A^\top\lambda$, the gradient of the Lagrangian in $x$.

The tests compare with `np.linalg.pinv`, check that adding any null-space vector to $x$ keeps it feasible and makes it longer, and that the multipliers measure how the optimal value moves with $b$: $\partial f^\star/\partial b = -\lambda$.

## Hints

1. `np.linalg.solve(A @ A.T, b)`.
2. A null-space direction: a vector $z$ with $Az = 0$, for example $z = v - A^\top(AA^\top)^{-1}Av$ for any $v$.
3. The optimal value is $\frac12 b^\top(AA^\top)^{-1}b$.

# The dual of a quadratic program

For $\min \frac12 x^\top Qx + c^\top x$ subject to $Ax \le b$, with $Q$ positive definite, minimizing the Lagrangian over $x$ in closed form gives $x(\lambda) = -Q^{-1}(c + A^\top\lambda)$ and the **dual function**

$$
d(\lambda) = -\tfrac12(c + A^\top\lambda)^\top Q^{-1}(c + A^\top\lambda) - b^\top\lambda ,
$$

concave, with gradient $\nabla d(\lambda) = Ax(\lambda) - b$: the constraint violation (Section 3).

- `dual_value(Q, c, A, b, lam)`, `dual_grad(Q, c, A, b, lam)` and `primal_value(Q, c, x)`.
- `dual_ascent(Q, c, A, b, step, iters)`: projected gradient ascent on $\lambda \ge 0$ from 0; return $\lambda$ and $x(\lambda)$.

The tests run a **gradient check** of `dual_grad`, confirm **weak duality** ($d(\lambda) \le p(x)$ for every $\lambda \ge 0$ and feasible $x$), and **strong duality** at the optimum: the gap closes.

## Hints

1. Solve with `np.linalg.solve(Q, ...)` rather than inverting.
2. Projection onto $\lambda \ge 0$ is `np.maximum(lam, 0)`.
3. A step below $1/\lambda_{\max}(AQ^{-1}A^\top)$ is safe.

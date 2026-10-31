# A KKT checker

For $\min f(x)$ subject to $g_j(x) \le 0$, a point $x$ with multipliers $\lambda$ is optimal for a convex problem exactly when the four **KKT conditions** hold (Section 2): stationarity $\nabla f + \sum_j\lambda_j\nabla g_j = 0$, primal feasibility $g_j \le 0$, dual feasibility $\lambda_j \ge 0$, and complementary slackness $\lambda_j g_j = 0$.

- `kkt_residuals(grad_f, grads_g, g_vals, lam)`: given the gradient of $f$ at $x$, the gradients of the constraints as rows of an array, their values and the multipliers, return a dict with the four residuals `"stationarity"` (norm), `"primal"` ($\max_j \max(g_j, 0)$), `"dual"` ($\max_j\max(-\lambda_j, 0)$) and `"slackness"` ($\max_j\lvert\lambda_j g_j\rvert$).
- `is_kkt(res, tol=1e-8)`: whether all four are at most `tol`.

The tests check the solution of a small quadratic program, then the same point with a multiplier on an inactive constraint, and an infeasible point.

## Hints

1. `grad_f + grads_g.T @ lam` is the gradient of the Lagrangian.
2. With no constraints active, every multiplier must be 0.
3. Return plain floats.

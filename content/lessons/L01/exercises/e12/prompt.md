# Newton's method for logistic regression

Use curvature (Section 3) to converge in a handful of iterations. Include the intercept as a column of ones in `X`. With an L2 penalty $\tfrac{\lambda}{2}\|w\|^2$:

$$
g = \tfrac1n X^\top(\sigma(Xw) - y) + \lambda w, \qquad H = \tfrac1n X^\top S X + \lambda I, \quad S = \operatorname{diag}\big(\sigma(1 - \sigma)\big).
$$

- `newton(X, y, l2, iters)`: start from zero, iterate $w \leftarrow w - H^{-1}g$, and return `(w, grad_norms)` where `grad_norms[k]` is $\|g\|$ before step $k$.

The tests check convergence to a gradient norm below $10^{-10}$ within 10 iterations, agreement with a long gradient-descent run, and the quadratic convergence signature.

## Hints

1. `S = s * (1 - s)`; `H = (X * S[:, None]).T @ X / n + l2 * np.eye(d)`.
2. Solve with `np.linalg.solve(H, g)` rather than inverting.
3. Quadratic convergence: once close, each gradient norm is roughly a constant times the square of the previous one.

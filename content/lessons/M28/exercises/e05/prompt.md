# Smoothness, strong convexity and the condition number

A function is **$L$-smooth** when its Hessian never exceeds $L$ in any direction, and **$\mu$-strongly convex** when it is never below $\mu$ (Section 4). For a quadratic $\frac12 x^\top A x - b^\top x$, $L$ and $\mu$ are the largest and smallest eigenvalues of $A$, and $\kappa = L/\mu$ is the **condition number**, the elongation of its level sets.

- `smooth_strong(A)`: the pair $(L, \mu)$ for a symmetric positive definite `A`.
- `condition_number(A)`: $L/\mu$.
- `logistic_smoothness(X)`: an upper bound on the logistic loss's smoothness, $\lambda_{\max}(X^\top X)/(4n)$, because $\sigma' \le \frac14$.
- `level_set_axes(A, c=1.0)`: the half-lengths of the ellipse $\frac12 x^\top A x = c$ along the eigenvectors, longest first, $\sqrt{2c/\lambda_i}$.

The tests connect the numbers: the ratio of the longest to the shortest axis is $\sqrt\kappa$, so a valley ten times narrower has a condition number a hundred times larger.

## Hints

1. `np.linalg.eigvalsh` returns eigenvalues in increasing order.
2. The Hessian of the logistic loss is $\frac1n X^\top D X$ with $D = \operatorname{diag}(\sigma(1 - \sigma)) \preceq \frac14 I$.
3. The longest axis belongs to the smallest eigenvalue.

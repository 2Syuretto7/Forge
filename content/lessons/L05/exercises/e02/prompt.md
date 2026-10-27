# Ridge regression as a MAP estimate

Implement Section 2.

- `ridge(X, y, lam)`: $(X^\top X + \lambda I)^{-1}X^\top y$ via `np.linalg.solve`.
- `map_objective(w, X, y, sigma2, tau2)`: the negative log-posterior up to constants, $\frac{1}{2\sigma^2}\|y - Xw\|^2 + \frac{1}{2\tau^2}\|w\|^2$.
- `effective_condition(X, lam)`: the condition number of $X^\top X + \lambda I$.

The tests check that `ridge(X, y, sigma2/tau2)` minimizes `map_objective`, that the weight norm shrinks as $\lambda$ grows, and that regularization cures an ill-conditioned problem.

## Hints

1. `np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y)`.
2. Setting the gradient of the MAP objective to zero gives the ridge equations with $\lambda = \sigma^2/\tau^2$.
3. Use `np.linalg.cond`.

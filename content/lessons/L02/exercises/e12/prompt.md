# Effective degrees of freedom of ridge

Section 3 measured a ridge model's capacity by $\mathrm{df}(\lambda) = \sum_j s_j^2/(s_j^2 + \lambda)$, where $s_j$ are the singular values of $X$.

- `df_svd(X, lam)`: the formula above.
- `df_trace(X, lam)`: $\operatorname{tr}\big(X(X^\top X + \lambda I)^{-1}X^\top\big)$ computed directly.
- `ddf_dlam(X, lam)`: the derivative of $\mathrm{df}$ with respect to $\lambda$, which you derive; the test checks it by finite differences.

## Hints

1. `s = np.linalg.svd(X, compute_uv=False)`.
2. The hat matrix is `X @ np.linalg.solve(X.T @ X + lam * I, X.T)`.
3. Differentiate $s^2/(s^2 + \lambda)$ term by term.

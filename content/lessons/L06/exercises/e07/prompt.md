# Minimum-norm interpolation and implicit regularization

With more features than points ($p > n$):

- `min_norm(X, y)`: $X^\top(XX^\top)^{-1}y$.
- `mse(w, X, y)` and `mse_grad(w, X, y)` for $\tfrac1n\|Xw - y\|^2$.
- `gd_from_zero(X, y, lr, steps)`: gradient descent on the MSE from $w = 0$.

The tests check that the minimum-norm solution interpolates, that adding any null-space vector keeps the fit but increases the norm, and that gradient descent from zero converges to the minimum-norm solution (Section 4).

## Hints

1. Solve with `np.linalg.solve(X @ X.T, y)` and multiply by `X.T`.
2. A null-space vector: take any `v` and subtract its projection onto the row space.
3. With `lr` below $1/\lambda_{\max}(\tfrac2n X X^\top)$, a few thousand steps converge.

# Gradient descent for linear regression

Minimize $L(w) = \tfrac1n\|Xw - y\|^2$ iteratively.

- `mse(w, X, y)` and `mse_grad(w, X, y)` $= \tfrac2n X^\top(Xw - y)$.
- `gd(X, y, lr, steps)`: from $w = 0$; return `(w, losses)` with the loss recorded before each step.
- `max_stable_lr(X)`: $2/\lambda_{\max}$ of the Hessian $\tfrac2n X^\top X$.

## Hints

1. The Hessian's top eigenvalue: `np.linalg.eigvalsh(2 / n * X.T @ X).max()`.
2. Learning rates just below `max_stable_lr` converge; just above diverge.
3. Use the same gradient-check pattern as in M15 and M18.

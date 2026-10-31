# Generalization gaps for 200 model sizes

Fit random-features regression, $\hat y = \sum_{j \le p}\beta_j\operatorname{relu}(w_j^\top x)$, to $n = 100$ noisy training points from the starter's `make_task()`, for every number of features $p$ from 1 to 200, with the minimum-norm least-squares solution (`np.linalg.lstsq`). Measure training and test error for each $p$ (Section 4, and BiasVarianceCurve in L02).

- `ridge_loss(beta, F, y, lam)` and `ridge_grad(beta, F, y, lam)`: $\frac1n\lVert F\beta - y\rVert^2 + \lambda\lVert\beta\rVert^2$ and its gradient.
- `curves(lam=0.0)`: for $p = 1, \dots, 200$, the training and test mean squared errors as two arrays. With `lam = 0` use `np.linalg.lstsq`; with `lam > 0` solve the ridge normal equations.

The tests run a **gradient check** of `ridge_grad`, then find the **double descent**: the test error peaks at $p = n = 100$, where the training error first reaches 0 and the minimum-norm interpolant is forced through the noise, and falls again beyond it. A small ridge penalty removes the peak.

## Hints

1. Features: `np.maximum(X @ W[:, :p], 0)` with the starter's fixed `W`.
2. Ridge: `np.linalg.solve(F.T @ F + n * lam * np.eye(p), F.T @ y)`.
3. The gap, test minus training error, is largest at the peak, where no bound based on counting parameters predicts the recovery that follows.

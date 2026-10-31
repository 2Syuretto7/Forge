# Gradient descent on a quadratic with a chosen spectrum

On $f(x) = \frac12 x^\top A x - b^\top x$, gradient descent with step $\eta$ moves the error $e = x - x^\star$ by $e \leftarrow (I - \eta A)e$: in the eigenvector basis each component is multiplied by $1 - \eta\lambda_i$ per step (Section 4).

- `make_quadratic(eigs, seed)`: a symmetric matrix with the given eigenvalues and random eigenvectors, the $Q$ factor of the QR decomposition of a `np.random.default_rng(seed)` standard normal matrix.
- `gd_errors(A, b, x0, step, iters)`: run `iters` steps and return the array of error norms $\lVert x_k - x^\star\rVert$, $k = 0, \dots, $ `iters`, with $x^\star$ from `np.linalg.solve`.
- `rate(eigs, step)`: the worst contraction factor $\rho = \max_i \lvert 1 - \eta\lambda_i\rvert$.

The tests compare the measured decay with $\rho$ for the steps $1/L$ (where $\rho = 1 - 1/\kappa$) and $2/(L + \mu)$ (where $\rho = \frac{\kappa - 1}{\kappa + 1}$, the best fixed step), and check that gradient descent does not care about the eigenvectors: a diagonal matrix with the same eigenvalues gives the same error norms.

## Hints

1. `Q, _ = np.linalg.qr(rng.standard_normal((d, d)))`, then `Q @ np.diag(eigs) @ Q.T`.
2. The gradient is $Ax - b$.
3. Measure the late rate as `(e[-1] / e[-11]) ** 0.1`, after the fast components have died.

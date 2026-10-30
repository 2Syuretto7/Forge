# The Rayleigh quotient as an average

For symmetric `S` and nonzero `x`:

- `rayleigh(S, x)`: $\rho(x) = x^\top S x / x^\top x$.
- `eig_weights(S, x)`: `(lam, w)` with `lam` the eigenvalues of `S` and `w[i]` $= c_i^2 / \|x\|^2$, where $c = Q^\top x$ are the coordinates of $x$ in the orthonormal eigenvector basis. The weights are nonnegative and sum to 1.

The tests check an **invariant**: $\rho(x) = \sum_i \lambda_i w_i$ and $\lambda_{\min} \leq \rho(x) \leq \lambda_{\max}$, for random matrices and vectors; and $\rho$ does not change when $x$ is scaled.

## Hints

1. `float(x @ S @ x / (x @ x))`.
2. `lam, Q = np.linalg.eigh(S)`, then `c = Q.T @ x`.
3. A weighted average of numbers lies between the smallest and the largest.

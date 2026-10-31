# The speed limit and the condition number

For a quadratic with symmetric positive definite Hessian $A$:

1. `rates(A)` returns a dictionary with `"kappa"` ($L/\mu$), `"lr_max"` ($2/L$), `"lr_opt"` ($2/(\mu + L)$) and `"rho_opt"` ($(\kappa - 1)/(\kappa + 1)$).
2. `contraction(A, lr)` returns $\max_i |1 - \eta\lambda_i|$, the worst-case factor by which one step multiplies the error.
3. `steps_needed(A, eps)` returns the smallest number of steps at `lr_opt` after which the worst-case error has shrunk by `eps`.

The tests compare all three with what gradient descent actually does.

## Hints

1. `np.linalg.eigvalsh` returns the eigenvalues of a symmetric matrix in ascending order.
2. The number of steps solves $\rho^t \le \epsilon$: $t = \lceil \ln\epsilon / \ln\rho \rceil$.
3. Rotating $A$ by an orthogonal matrix changes none of these numbers.

# The least-squares gradient, checked numerically

Implement the loss $L(x) = \|Ax - b\|^2$, its gradient $\nabla L(x) = 2A^\top(Ax - b)$ from Section 3, and gradient descent on it.

- `loss(x, A, b)` returns a float.
- `grad(x, A, b)` returns shape `(n,)`.
- `gd_solve(A, b, steps)`: start at $x = 0$ and take `steps` steps of $x \leftarrow x - \eta \nabla L(x)$ with step size $\eta = 1 / (2\sigma_{\max}^2)$, where $\sigma_{\max}$ is the largest singular value of `A` (`np.linalg.norm(A, 2)`). Return `x`.

The gradient check compares your formula against central finite differences, $\dfrac{L(x + h e_i) - L(x - h e_i)}{2h}$, and requires a relative error below $10^{-5}$. L09 explains where the step size comes from: $2\sigma_{\max}^2$ is the largest curvature of $L$.

## Hints

1. `r = A @ x - b`, then `loss = r @ r` and `grad = 2 * A.T @ r`.
2. Curvature: the Hessian of $L$ is $2A^\top A$, whose largest eigenvalue is $2\sigma_{\max}^2$.
3. Return Python floats from `loss`.

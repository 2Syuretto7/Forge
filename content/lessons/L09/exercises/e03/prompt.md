# Heavy-ball momentum

1. `heavy_ball(grad, x0, lr, beta, steps)` runs $v \leftarrow \beta v + \nabla f(x)$, $x \leftarrow x - \eta v$ from $v = 0$ and returns all iterates, shape `(steps + 1, d)`.
2. `tuned_heavy_ball(A)` returns the optimal `(lr, beta)` for a quadratic with Hessian $A$: $\eta = 4/(\sqrt L + \sqrt\mu)^2$ and $\beta = \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^2$.

The tests race tuned momentum against gradient descent at its optimal rate on a valley with condition number 100. Plain `gd` is provided.

## Hints

1. With `beta = 0` your function must reproduce `gd` exactly.
2. Update the velocity before the position, and evaluate the gradient at the current position.
3. Copy the position into the list at every step, or every entry will point to the same array.

# Adam, step 2: invariance to scale

Multiply the loss by a constant $c > 0$: every gradient is multiplied by $c$, $m$ by $c$ and $\sqrt v$ by $c$, and Adam's update does not change, apart from $\varepsilon$ (Section 4). Gradient descent's update is multiplied by $c$, so its learning rate must be retuned. Per coordinate, Adam divides by a running estimate of the gradient's size: a diagonal preconditioner learned on the fly.

- `run_adam(grad, x0, steps, lr)` and `run_sgd(grad, x0, steps, lr)`: trajectories, arrays of shape `(steps + 1, dim)`.
- `quadratic_grad(scales)`: a function returning the gradient of $\frac12\sum_is_ix_i^2$.

The tests show Adam's trajectory unchanged when the loss is scaled by 1,000 (to within $10^{-6}$), while gradient descent with the same learning rate diverges.

## Hints

1. Use $\varepsilon = 10^{-12}$ here so that it does not break the invariance at these scales.
2. Gradient descent on $\frac c2sx^2$ is stable only for a learning rate below $2/(cs)$ (M16).
3. Adam is invariant to a diagonal rescaling of the gradient only in the limit $\beta_2 \to 1$; with a constant factor it is exact.

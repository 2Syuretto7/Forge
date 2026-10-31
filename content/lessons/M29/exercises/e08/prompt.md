# Step-size schedules

A constant step leaves SGD in a cloud whose size is proportional to the step, so reaching the optimum needs a step that shrinks: the **Robbins-Monro** conditions $\sum_k\eta_k = \infty$ (the steps can travel any distance) and $\sum_k\eta_k^2 < \infty$ (the injected noise is finite) (Section 4).

- `inverse_time(k, eta0, k0)`: $\eta_0 k_0/(k + k_0)$.
- `step_decay(k, eta0, every, factor=0.5)`: $\eta_0\,\text{factor}^{\lfloor k/\text{every}\rfloor}$.
- `cosine(k, eta0, total)`: $\frac{\eta_0}{2}(1 + \cos(\pi k/\text{total}))$ for $k \le$ `total`.
- `sgd_scheduled(grad_sample, w0, schedule, iters, rng)`: SGD where `grad_sample(w, rng)` returns a stochastic gradient and `schedule(k)` the step; return the final iterate.

The tests run SGD on a one-dimensional quadratic with gradient noise: the constant step stalls at its floor, and the $1/k$ schedule goes far below it.

## Hints

1. Each schedule is a one-line function of the step index $k$, starting at $k = 0$.
2. $\sum 1/k$ diverges and $\sum 1/k^2$ converges: the inverse-time schedule satisfies both conditions.
3. Average the squared final error over many runs to compare schedules fairly. Pass a vector `w0` to run them all at once: every operation is elementwise.

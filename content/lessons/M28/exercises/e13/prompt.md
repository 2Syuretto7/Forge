# Break it: a step past 2/L

On an $L$-smooth function, gradient descent with step $\eta$ multiplies the error along the steepest direction by $1 - \eta L$. Past $\eta = 2/L$ that factor is below $-1$: every step overshoots by more than the last, and the iterates oscillate with growing amplitude (Section 4, and M16's step-size limit).

- `gd_path(A, x0, step, iters)`: the iterates of gradient descent on $\frac12 x^\top A x$, as an array of shape `(iters + 1, d)`.
- `growth_factor(A, step)`: $\max_i \lvert 1 - \eta\lambda_i\rvert$; above 1 means divergence.
- `largest_stable_step(A)`: $2/\lambda_{\max}$.

The tests run at 1.9/L and 2.1/L, watch the steep coordinate shrink in one and explode in the other while changing sign every step, and see the shallow coordinate converge in both: divergence is decided by the steepest direction alone.

## Hints

1. With $A$ diagonal, coordinate $i$ evolves as $x_i \leftarrow (1 - \eta\lambda_i)x_i$.
2. Sign changes: `np.sign(path[1:, i]) != np.sign(path[:-1, i])`.
3. In a network, the steepest direction is set by the largest Hessian eigenvalue, which is why warm-up and gradient clipping exist (L05).

# The tangent plane lies below

A differentiable convex function lies above every tangent plane: $f(y) \ge f(x) + \nabla f(x)^\top(y - x)$ (Section 2). This is why a zero gradient certifies a global minimum.

Take the logistic regression loss on data $X$ (rows) and labels $y \in \{0, 1\}$:

$$
L(w) = \frac1n\sum_i \big[\operatorname{softplus}(x_i^\top w) - y_i\,x_i^\top w\big] .
$$

- `logistic_loss(w, X, y)`, with M26's stable softplus.
- `logistic_grad(w, X, y)`: $\frac1n X^\top(\sigma(Xw) - y)$.
- `tangent_gap(f, grad, x, y_point)`: $f(y) - f(x) - \nabla f(x)^\top(y - x)$, which is at least 0 for convex $f$.

The tests run a **gradient check** of `logistic_grad`, and confirm that the tangent gap is never negative for random pairs of weight vectors, while it is negative somewhere for a non-convex function.

## Hints

1. $\operatorname{softplus}(z) = \max(z, 0) + \log(1 + e^{-\lvert z\rvert})$.
2. The gradient of $\operatorname{softplus}(z)$ is $\sigma(z)$; compute $\sigma$ stably from $e^{-\lvert z\rvert}$.
3. M25: this loss is the negative log-likelihood of a Bernoulli model, and its convexity is that of an exponential family.

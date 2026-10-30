# Stale gradients

The starter provides the reverse-mode engine of e01 (`Var`, `backward`), which accumulates gradients with `+=`. Accumulation is right within one backward pass, and wrong across passes unless the gradients are reset.

- `square_grad(x)`: $\frac{d}{dx}(x \cdot x)$ through the engine, one multiplication node whose arguments are the same `Var`: it must be $2x$.
- `fit_line(xs, ys, steps, lr, zero_grads)`: fit $y \approx wx + b$ by gradient descent on the mean squared error, with `w` and `b` as `Var`s that persist across steps; at each step build the loss, call `backward`, update `w.value` and `b.value`; if `zero_grads`, set both `grad`s to 0 before each backward pass. Return `(w, b)` as floats.

Without zeroing, each step uses the sum of all past gradients: momentum without decay, and the fit oscillates and diverges.

## Hints

1. `x = Var(3.0); y = x * x; backward(y); x.grad`.
2. Build the loss as a sum of `Var`s over the data points, divided by their number.
3. A learning rate of 0.05 on data with $x$ in $[0, 1]$ converges when gradients are zeroed.

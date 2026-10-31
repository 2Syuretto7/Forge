# Loss scaling

1. `underflow_fraction(grads, scale=1.0)`: the fraction of nonzero float32 gradients that become exactly zero when `grads * scale` is cast to float16.
2. `scaled_loss_and_grad(w, X, y, scale)`: for the least-squares loss $L = \tfrac12 \operatorname{mean}((Xw - y)^2)$, return the scaled loss $S \cdot L$ and its gradient $S\, \partial L/\partial w$, which is what the backward pass produces when the loss is multiplied by $S$ first.

The tests use gradients spread over many orders of magnitude around $10^{-7}$, as late in training.

## Hints

1. Multiply in float32 before casting: `(g * np.float32(scale)).astype(np.float16)`.
2. Dividing the scaled gradient by $S$ recovers the true gradient exactly when $S$ is a power of two.
3. Too large a scale overflows instead; dynamic scaling (exercise 6) searches for the largest safe one.

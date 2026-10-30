# VJPs of the tensor operations in a layer

A linear layer with bias computes $Y = XW + b$, with $b$ broadcast over the batch. For an upstream gradient $G = \partial L/\partial Y$:

- `matmul_backward(X, W, G)`: `(dX, dW)` with $dX = GW^\top$ and $dW = X^\top G$.
- `bias_backward(G)`: $\partial L/\partial b$: the forward pass broadcast $b$ over the batch, so the backward pass **sums** over it.
- `relu_backward(Z, G)`: for $A = \max(0, Z)$, the gradient $G \odot \mathbb{1}[Z > 0]$.
- `mse_backward(P, T)`: for $L = \frac{1}{N}\sum (P - T)^2$ over all $N$ entries, $\frac{2}{N}(P - T)$.

The tests run a **gradient check** of a whole two-layer network assembled from these pieces.

## Hints

1. Shapes: `dW` like `W`, `dX` like `X`, `db` like `b`.
2. `G.sum(axis=0)`.
3. `(Z > 0) * G`.

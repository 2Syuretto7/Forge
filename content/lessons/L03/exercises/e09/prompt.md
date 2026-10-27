# Gradients of a matrix product

For $Y = XW$ with $X \in \mathbb{R}^{B \times n}$ and $W \in \mathbb{R}^{n \times m}$, and upstream gradient $G = \partial L/\partial Y$, implement Section 6's result:

- `matmul_backward(X, W, G)` returns `(dX, dW)` with $dX = GW^\top$ and $dW = X^\top G$.
- `loss(X, W, G)`: the scalar $L = \sum_{b,j} G_{bj} Y_{bj}$, whose gradient with respect to $Y$ is exactly $G$. The tests use it to check your formulas by finite differences.

Shapes are part of the check: `dX` must have the shape of `X` and `dW` the shape of `W`.

## Hints

1. `np.sum(G * (X @ W))` is the loss.
2. Match shapes: $(B \times m)(m \times n)$ gives $B \times n$.
3. These two lines are the backward pass of every linear layer you will write.

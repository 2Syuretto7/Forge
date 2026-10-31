# Fusing a bias and an activation

`gelu(x)` (tanh approximation) is provided.

1. `gelu_grad(x)`: its derivative.
2. `bias_gelu_forward(x, b)` returns `(gelu(x + b), cache)` for `x` of shape `(N, d)` and bias `b` of shape `(d,)`; `bias_gelu_backward(dy, cache)` returns `(dx, db)`.
3. `traffic(n, bytes_per=2, fused=True)`: bytes moved for $n$ elements, ignoring the small bias vector. Unfused, one kernel reads `x` and writes `z = x + b`, and a second reads `z` and writes `y`: $4n$ values. Fused, one kernel reads `x` and writes `y`: $2n$ values.

## Hints

1. With $u = c(x + 0.044715x^3)$ and $t = \tanh u$: $\operatorname{gelu}'(x) = \tfrac12(1 + t) + \tfrac12 x (1 - t^2)\, c\,(1 + 3 \cdot 0.044715 x^2)$.
2. Cache $z = x + b$; the bias gradient sums over the batch.
3. The fused kernel moves half the bytes, so the memory-bound pair runs about twice as fast.

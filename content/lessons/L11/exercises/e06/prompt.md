# The backward pass costs twice the forward

1. `matmul_backward(dY, X, W)`: for $Y = XW$, return $(\partial L/\partial X, \partial L/\partial W)$.
2. `step_flops(batch_tokens, layer_shapes)`: FLOPs of one training step through linear layers with the given `(n_in, n_out)` shapes: $2 \cdot \text{tokens} \cdot n_{\text{in}} n_{\text{out}}$ per layer forward, and two matrix products of that size per layer backward.
3. `flops_per_token_per_param()`: the constant $c$ in "training costs about $c$ FLOPs per token per parameter".

## Hints

1. $\partial L/\partial X = (\partial L/\partial Y) W^\top$ and $\partial L/\partial W = X^\top (\partial L/\partial Y)$.
2. Each backward product has the same size as the forward one.
3. Divide `step_flops` by tokens times parameters to find the constant.

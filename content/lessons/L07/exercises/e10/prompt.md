# Recompute instead of store

`gelu` and `gelu_grad` are provided. For the block $y = \operatorname{gelu}(xW_1)W_2$:

1. `mlp_forward(x, W1, W2, store=True)` returns `(y, cache)`; the cache is `(x, h, a)` with $h = xW_1$ and $a = \operatorname{gelu}(h)$ when `store=True`, and only `(x,)` when `store=False`.
2. `mlp_backward(dy, cache, W1, W2)` returns `(dx, dW1, dW2)`, recomputing $h$ and $a$ from $x$ when they were not stored.

`cache_floats(cache)` (given) counts the numbers kept between the passes. With hidden width four times the input width, recomputation keeps a ninth of them, for one extra matrix product and GELU.

## Hints

1. Recompute exactly as in the forward pass, so the gradients match to the last bit.
2. `dW2 = a.T @ dy`, `dh = (dy @ W2.T) * gelu_grad(h)`, `dW1 = x.T @ dh`, `dx = dh @ W1.T`.
3. This is activation checkpointing, applied at the scale of one block; L14 applies it to whole layers.

# One-pass statistics and a fused layer-norm backward

A fused layer-norm kernel computes each row's mean and variance in one pass over the row.

1. `naive_moments(x)`: mean and variance as $\mathbb E[x^2] - \mathbb E[x]^2$, accumulating in the array's own dtype.
2. `welford(x)`: mean and variance with Welford's update, also in the array's dtype.
3. `layernorm_backward_recompute(dy, x, gamma, eps=1e-5)`: the layer-norm backward pass of L10, recomputing the mean and $1/\sigma$ from `x` instead of storing them, as a fused backward kernel does. Return `(dx, dgamma, dbeta)`.

The tests feed float32 values near $10^4$ with unit spread: the naive variance cancels to garbage, Welford's does not.

## Hints

1. Use `x.dtype.type(...)` for constants so the arithmetic stays in float32.
2. Welford: `d = v - mean; mean += d / i; m2 += d * (v - mean)`; the variance is `m2 / n`.
3. The backward formula: with `g = dy * gamma`, `dx = r / d * (d * g - g.sum(1) - xh * (g * xh).sum(1))` (keepdims).

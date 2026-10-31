# Layer norm, forward and backward

Implement layer norm for `x` of shape `(N, d)`: the same computation as batch norm, but each **row** is normalized over its features, and `gamma`, `beta` have shape `(d,)`.

1. `layernorm_forward(x, gamma, beta, eps=1e-5)` returns `(y, cache)`.
2. `layernorm_backward(dy, cache)` returns `(dx, dgamma, dbeta)`.

## Hints

1. Use `axis=1, keepdims=True` for the statistics.
2. `dgamma` and `dbeta` still sum over the batch (axis 0): every row uses the same `gamma` and `beta`.
3. The input gradient is the batch-norm formula with `d` in place of `N` and sums over axis 1.

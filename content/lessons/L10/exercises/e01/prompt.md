# Batch norm, forward and backward

Implement training-mode batch norm for `x` of shape `(N, d)`:

1. `batchnorm_forward(x, gamma, beta, eps=1e-5)` returns `(y, cache)`: normalize each column with the batch mean and (biased) variance, then scale by `gamma` and shift by `beta`.
2. `batchnorm_backward(dy, cache)` returns `(dx, dgamma, dbeta)` using the formula from the derivation.

## Hints

1. Cache `xh`, `r = 1 / sqrt(var + eps)` and `gamma`; nothing else is needed.
2. `dgamma = (dy * xh).sum(axis=0)` and `dbeta = dy.sum(axis=0)`.
3. With `g = dy * gamma`: `dx = r / N * (N * g - g.sum(axis=0) - xh * (g * xh).sum(axis=0))`.

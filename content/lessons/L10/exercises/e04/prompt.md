# RMSNorm, forward and backward

Implement RMSNorm for `x` of shape `(N, d)`: $y = \gamma \odot x / r$ with $r = \sqrt{\tfrac1d \sum_j x_j^2 + \epsilon}$ per row, and no shift.

1. `rmsnorm_forward(x, gamma, eps=1e-6)` returns `(y, cache)`.
2. `rmsnorm_backward(dy, cache)` returns `(dx, dgamma)`, with $\partial L/\partial x_j = g_j / r - x_j \sum_k g_k x_k / (d r^3)$ where $g = \gamma \odot \partial L/\partial y$.

## Hints

1. Keep `r` with shape `(N, 1)` so it broadcasts over the features.
2. `dgamma = (dy * x / r).sum(axis=0)`.
3. Derive the input gradient yourself first: $r$ depends on every $x_k$ through $\partial r/\partial x_k = x_k/(d r)$.

# The layer-normalization Jacobian

For $x \in \mathbb{R}^d$, layer normalization (without its learned scale and shift) computes $\hat x = (x - \mu)/\sigma$ with $\mu = \bar x$ and $\sigma = \sqrt{\overline{(x - \mu)^2} + \varepsilon}$.

- `layernorm(x, eps)` returns $\hat x$.
- `layernorm_vjp(x, u, eps)` returns $u^\top \partial \hat x / \partial x$ using the formula of Section 6, $\frac{1}{\sigma}\big(u - \bar u - \overline{u \odot \hat x}\,\hat x\big)$. This formula is exact for any $\varepsilon$ when $\hat x$ is computed with that same $\varepsilon$.
- `layernorm_jacobian(x, eps)`: the full $d \times d$ matrix, built from the VJP applied to each unit vector.

The tests check the VJP against finite differences and verify two invariances: shifting $x$ by a constant changes nothing (so $J\mathbf{1} = 0$), and with $\varepsilon = 0$ scaling $x$ changes nothing (so $Jx = 0$).

## Hints

1. Compute `xh = layernorm(x, eps)` and `sigma` once.
2. `(u - u.mean() - (u * xh).mean() * xh) / sigma`.
3. Row $i$ of $J$ is the VJP with $u = e_i$.

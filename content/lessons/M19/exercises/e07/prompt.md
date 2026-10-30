# The softmax Jacobian and its fast VJP

Implement Section 6's softmax results for a 1-D logit vector `z`.

- `softmax(z)`: numerically stable.
- `softmax_jacobian(z)`: $\operatorname{diag}(p) - pp^\top$, shape `(K, K)`.
- `softmax_vjp(z, u)`: $u^\top J = p \odot (u - u^\top p)$ in $O(K)$ work, without forming $J$.

## Hints

1. Subtract `z.max()` before exponentiating.
2. `np.diag(p) - np.outer(p, p)`.
3. Because $J$ is symmetric, the VJP and the JVP are the same vector.

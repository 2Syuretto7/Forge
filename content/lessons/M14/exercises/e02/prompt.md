# The SVD by power iteration and deflation

- `top_singular(A, iters=500, seed=0)`: power iteration on $A^\top A$ without forming it (multiply by $A$, then by $A^\top$), from a seeded random vector. Return `(sigma, u, v)` with $v$ the final unit vector, $\sigma = \|Av\|$ and $u = Av/\sigma$.
- `svd_deflation(A, k, iters=500)`: the top `k` triplets, found one at a time: after each one, subtract $\sigma u v^\top$ from (a copy of) $A$ and repeat. Return `(U, s, Vt)` with shapes `(m, k)`, `(k,)`, `(k, n)`.

Each step shrinks the error by $(\sigma_2/\sigma_1)^2$, the squared gap of M13, because $A^\top A$ has eigenvalues $\sigma_i^2$.

## Hints

1. `v = A.T @ (A @ v)`, then normalize.
2. Deflation removes the top triplet, so the next power iteration finds the next one.
3. Signs are arbitrary: compare $\sigma$ values, and singular vectors up to sign.

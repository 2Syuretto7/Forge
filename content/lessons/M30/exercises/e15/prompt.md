# Break it: duality without convexity

Weak duality holds for every problem; strong duality needs convexity (Section 3). Take a problem that is not convex: minimize $x^\top Wx$ over $x \in \{-1, +1\}^n$, the max-cut problem in disguise. Write the constraints as $x_i^2 = 1$; the Lagrangian $x^\top Wx - \sum_i\nu_i(x_i^2 - 1)$ is bounded below in $x$ only when $W - \operatorname{diag}(\nu) \succeq 0$, and choosing $\nu_i = \lambda_{\min}(W)$ for every $i$ gives the lower bound

$$
d = n\,\lambda_{\min}(W) \le p^\star .
$$

- `brute_force(W)`: $p^\star$ by trying all $2^n$ sign vectors (for $n \le 12$).
- `eigen_bound(W)`: $n\lambda_{\min}(W)$.
- `gap(W)`: $p^\star - d$, which is positive for a typical random $W$.

The tests confirm the bound on random matrices with $n = 10$, find a strictly positive gap, and find no gap when $W$ is a multiple of the identity, where every sign vector is optimal. (Choosing a different $\nu_i$ for each $i$ can tighten the bound, which is then a semidefinite program; for a random $W$ a gap remains.)

## Hints

1. All sign vectors: `np.array(list(itertools.product([-1, 1], repeat=n)))`, then `np.einsum("ki,ij,kj->k", S, W, S)`.
2. `np.linalg.eigvalsh(W)[0]`.
3. Symmetrize random matrices first: `(M + M.T) / 2`.

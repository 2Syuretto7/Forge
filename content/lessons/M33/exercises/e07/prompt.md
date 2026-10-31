# The randomized range finder

To find the dominant column space of $A$ ($m \times n$), multiply it by a thin random matrix: $Y = A\Omega$ with $\Omega$ Gaussian of shape $n \times (k + p)$, then orthonormalize, $Q = \mathrm{qr}(Y)$ (Section 5). Each column of $Y$ is a random combination of $A$'s columns, so the top singular directions dominate it. The $p$ extra columns, the **oversampling**, make missing a direction unlikely, and Halko, Martinsson and Tropp proved

$$
\mathbb{E}\lVert A - QQ^\top A\rVert_F \le \sqrt{1 + \frac k{p - 1}}\,\Big(\sum_{j > k}\sigma_j^2\Big)^{1/2} .
$$

- `range_finder(A, k, p, rng)`: $Q$ with $k + p$ orthonormal columns.
- `power_range_finder(A, k, p, q, rng)`: the same with $q$ power iterations, multiplying by $A^\top$ then $A$ and re-orthonormalizing after each product.
- `projection_error(A, Q)`: $\lVert A - QQ^\top A\rVert_F$.
- `tail_norm(s, k)`: $(\sum_{j > k}\sigma_j^2)^{1/2}$ for singular values `s` in decreasing order.
- `hmt_factor(k, p)`: $\sqrt{1 + k/(p - 1)}$.

The tests compare your errors with the optimum from Eckart-Young (M14) and the bound, and show power iterations closing the gap on a slowly decaying spectrum.

## Hints

1. `np.linalg.qr(Y)[0]` returns the thin $Q$.
2. Power iterations replace the singular values $\sigma_j$ by $\sigma_j^{2q+1}$, which makes a slowly decaying spectrum decay fast.
3. Re-orthonormalize between products, or rounding erases every direction but the first.

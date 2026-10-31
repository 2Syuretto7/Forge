# Break it: no oversampling, slow decay

The randomized SVD's guarantee has two levers, oversampling $p$ and power iterations $q$ (Section 5). Remove both, on a matrix whose singular values decay slowly, and the approximation is far from optimal even though nothing reports an error.

- `rsvd_error_ratio(A, s, k, p, q, rng)`: the Frobenius error of e08's randomized SVD of rank $k$ divided by the optimal error $(\sum_{j > k}\sigma_j^2)^{1/2}$.
- `spectral_error_ratio(A, s, k, p, q, rng)`: the same in the spectral norm, $\lVert A - A_k\rVert_2/\sigma_{k+1}$, where the Frobenius ratio hides the damage behind a long tail.
- `make_matrix(m, n, decay, rng)` is provided, with singular values $1/j^{\text{decay}}$.

The tests find the spectral ratio near 2 with $p = 0$, $q = 0$ on singular values $1/\sqrt j$, and near 1 with $p = 10$, $q = 2$.

## Hints

1. With $p = 0$ the bound of e07 has $p - 1 < 0$ in a denominator: there is no guarantee at all.
2. `np.linalg.norm(M, 2)` is the spectral norm.
3. The spectral norm sees the largest missed direction; the Frobenius norm averages it into a tail that is large whatever you do.

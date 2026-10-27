# Low-rank compression and the Eckart-Young error

Treat a grayscale image as a matrix and compress it by truncating its SVD.

- `rank_k_approx(A, k)`: the truncated SVD $A_k = \sum_{i \le k} \sigma_i u_i v_i^\top$.
- `eckart_young_error(s, k)`: given **all** singular values `s` (descending), return $\|A - A_k\|_F$ without forming any matrix.
- `compression_ratio(m, n, k)`: storing $A$ costs $mn$ numbers; storing $A_k$ costs $k(m + n + 1)$. Return the ratio of the first to the second.
- `smallest_k(A, rel_tol)`: the smallest $k \ge 0$ with $\|A - A_k\|_F / \|A\|_F \le$ `rel_tol`.

One test builds random rank-$k$ competitors and checks that none of them beats your $A_k$.

## Hints

1. `U, s, Vt = np.linalg.svd(A, full_matrices=False)`; then `(U[:, :k] * s[:k]) @ Vt[:k]`.
2. The error is `np.sqrt(np.sum(s[k:] ** 2))`.
3. For `smallest_k`, compare the tail sums of `s**2` with `rel_tol**2 * sum(s**2)`.

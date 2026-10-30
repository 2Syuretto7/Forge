# The SVD from the eigenvectors of A transpose A

Implement Section 1 directly. For `A` of shape `(m, n)`:

1. Eigen-decompose $A^\top A$ with `np.linalg.eigh` (eigenvalues come out ascending).
2. Sort descending, clip tiny negative eigenvalues to 0, and set $\sigma_i = \sqrt{\lambda_i}$.
3. Keep only the $r$ components with $\lambda_i > 10^{-12}\,\lambda_1$, that is $\sigma_i > 10^{-6}\,\sigma_1$ (the numerical rank). The threshold cannot be tighter: rounding errors in the entries of $A^\top A$ are about $\varepsilon \lambda_1$, so an exact zero singular value comes out as roughly $\sqrt{\varepsilon}\,\sigma_1 \approx 10^{-8}\sigma_1$.
4. Set $u_i = A v_i / \sigma_i$.

Return `U` `(m, r)`, `s` `(r,)` descending, `Vt` `(r, n)`, so that `U @ np.diag(s) @ Vt` reconstructs `A`. Do not call `np.linalg.svd`.

This route squares the condition number, so it is only accurate for well-conditioned matrices. The tests check an **invariant** on random well-conditioned matrices of every shape: the factors reconstruct $A$ and have orthonormal columns. Movement 5 shows the failure mode.

## Hints

1. `w, V = np.linalg.eigh(A.T @ A)`, then `order = np.argsort(w)[::-1]`.
2. `U = (A @ V[:, :r]) / s[:r]` divides each column by its singular value.
3. Rank-deficient inputs must return fewer than `min(m, n)` components.

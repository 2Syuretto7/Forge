# Randomized SVD

With an orthonormal $Q$ that captures the range of $A$, the small matrix $B = Q^\top A$ of shape $(k + p) \times n$ holds everything: take its SVD, $B = \tilde U\Sigma V^\top$, and $A \approx (Q\tilde U)\Sigma V^\top$ (Section 5). The expensive steps are matrix products, which run near the compute roof; the only full SVD is of a small matrix.

- `rsvd(A, k, p=10, q=1, rng=None)`: `(U, s, Vt)` of the rank-$k$ approximation, with `U` of shape $m \times k$, `s` of length $k$ and `Vt` of shape $k \times n$. Use e07's range finder with $q$ power iterations.
- `top_singular_value(A)` and `grad_top_singular_value(A)`: $\sigma_1$ and its gradient with respect to the entries of $A$, which is $u_1v_1^\top$ when $\sigma_1$ is simple: perturbing $A$ by $E$ changes $\sigma_1$ by $u_1^\top Ev_1$ to first order.

The tests compare `rsvd` with the full SVD on a matrix of exact rank plus small noise, and run a **gradient check** of $\sigma_1$.

## Hints

1. `np.linalg.svd(B, full_matrices=False)` on the small matrix, then keep the first $k$ components.
2. The signs of singular vectors are arbitrary; compare singular values, or the reconstructed matrices.
3. For the gradient, $\sigma_1 = u_1^\top Av_1$, and the first-order changes of $u_1$ and $v_1$ do not contribute because they are orthogonal to $u_1$ and $v_1$.

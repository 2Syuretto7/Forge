# Two dimensions

Everything carries over to $\mathbb R^2$ (Section 8). A mixture of isotropic Gaussians with means $m_k$ and standard deviation $s$ has score $\sum_kr_k(x)(m_k - x)/s^2$; under the forward process its components move to $e^{-t}m_k$ with variance $s^2e^{-2t} + 1 - e^{-2t}$; and the reverse SDE runs coordinate by coordinate with the vector score.

- `mixture2d_logpdf(X, w, M, s)` and `mixture2d_score(X, w, M, s)` for points `X` of shape `(n, 2)`, means `M` of shape `(K, 2)` and a common standard deviation `s`.
- `noised_score(X, t, w, M, s)`: the exact score at time $t$.
- `reverse_sample_2d(score, n, T, steps, rng, tmin=1e-3)`: as e07, on a geometric grid.
- `sliced_w1(X, Y, rng, n_proj=50)`: the average over random directions of the one-dimensional $W_1$ between the projections, computed from 200 matching quantiles so the samples may differ in size.

The tests run a **gradient check** of the two-dimensional score and generate the three-component target of the capstone from noise, within a sliced distance of 0.08.

## Hints

1. `d = X[:, None, :] - M[None]` holds all differences, shape `(n, K, 2)`.
2. Directions $(\cos\phi, \sin\phi)$ with $\phi$ uniform on $[0, \pi)$ cover all projections.
3. `np.quantile(P, q, axis=0)` computes the quantiles of every projection at once.

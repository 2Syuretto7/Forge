# How many directions do embeddings need?

`make_embeddings(n, d, seed=0)` in the starter builds `n` points in `d` dimensions whose covariance has a power-law spectrum (variance along the $i$-th direction proportional to $i^{-1.2}$), plus a mean offset.

- `top_k_svd(X, k)`: the top `k` singular values and right singular vectors of the **centred** data from the eigen-decomposition of the $d \times d$ matrix $X_c^\top X_c$ (cheap when $d \ll n$): return `(s, Vt)` with shapes `(k,)` and `(k, d)`.
- `explained(s_all)`: the cumulative fraction of variance, `cumsum(s**2) / sum(s**2)`.
- `rank_for(s_all, fraction)`: the smallest $k$ whose cumulative fraction reaches `fraction`.
- `recon_error(X, Vt_k)`: the relative Frobenius error of reconstructing the centred data from the given components.

Try `make_embeddings(5000, 768)` in the console: no small $k$ explains 95 percent, the usual situation with real embeddings. The tests use 2,000 points in 128 dimensions.

## Hints

1. `w, V = np.linalg.eigh(Xc.T @ Xc)`, sorted descending; singular values are `sqrt(w)`.
2. Eckart-Young: the error of the top $k$ is $\sqrt{1 - \text{explained}[k-1]}$.
3. Reconstruct with `Xc @ Vt_k.T @ Vt_k`.

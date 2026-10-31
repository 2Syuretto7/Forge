# The best low-rank update

LoRA restricts the update to rank $r$. By the Eckart-Young theorem (M14's SVD), the best rank-$r$ approximation of a matrix in Frobenius norm is its truncated SVD, and the error is set by the discarded singular values.

1. `best_rank_r(M, r)`: the truncated SVD.
2. `relative_error(M, r)`: $\sqrt{\sum_{i > r} \sigma_i^2 / \sum_i \sigma_i^2}$.
3. `rank_for(M, tol)`: the smallest rank whose relative error is at most `tol`.

## Hints

1. `np.linalg.svd(M, full_matrices=False)` returns $U$, the singular values and $V^\top$.
2. `(U[:, :r] * S[:r]) @ Vt[:r]` keeps the top $r$ components.
3. Fine-tuning updates of large models are often close to low rank, which is why small $r$ works.

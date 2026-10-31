# LoRA, step 2: the best rank-r update

If the ideal fine-tuning update $\Delta W$ were known, the best rank-$r$ approximation to it in the Frobenius norm would be its truncated SVD, with error $(\sum_{j > r}\sigma_j^2)^{1/2}$ (M14, Section 3). LoRA's bet is that useful updates have small effective rank, so that this error is small for small $r$.

- `best_rank_r(M, r)`: the truncated SVD of `M`.
- `rank_r_error(M, r)`: its relative Frobenius error.
- `effective_rank(M, energy=0.9)`: the smallest $r$ capturing the fraction `energy` of $\sum\sigma_j^2$.

The tests build an update of exact rank 4 plus small noise and find rank 4 enough for a relative error below 3 percent, and the effective rank equal to 4.

## Hints

1. `U[:, :r] * s[:r] @ Vt[:r]`.
2. Cumulative sums of squared singular values give the captured energy.
3. A random full-rank update needs nearly all of its singular values; e10 shows LoRA failing there.

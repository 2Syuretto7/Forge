# LoRA, step 1: counting parameters

LoRA fine-tunes a weight matrix $W_0 \in \mathbb R^{k \times d}$ by adding a product of two thin matrices, $W = W_0 + BA$ with $B \in \mathbb R^{k \times r}$ and $A \in \mathbb R^{r \times d}$, and trains only $A$ and $B$ (Section 3). The update has rank at most $r$, and costs $r(k + d)$ parameters instead of $kd$.

- `lora_params(k, d, r)` and `full_params(k, d)`.
- `fraction(k, d, r)`: the ratio.
- `merged(W0, B, A)`: $W_0 + BA$, which can replace $W_0$ after training at no extra inference cost.
- `rank_of(M, tol=1e-9)`: the number of singular values above `tol` times the largest.

The tests check the counts for a $4096 \times 4096$ projection at rank 8, about 0.4 percent of the full matrix, and that the merged update's rank is at most $r$.

## Hints

1. A rank-$r$ product of a $k \times r$ and an $r \times d$ matrix has at most $r$ nonzero singular values (M14).
2. `np.linalg.svd(M, compute_uv=False)`.
3. Optimizer state scales with the trained parameters, which is where most of LoRA's memory saving comes from.

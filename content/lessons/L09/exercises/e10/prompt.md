# Attention memory and intensity

1. `score_bytes(batch, heads, n_ctx, bytes_per=2)`: memory of one layer's attention weights.
2. `scores_intensity(n_ctx, d_head, bytes_per=2)`: arithmetic intensity of computing $S = QK^\top$ for one head ($2n^2d$ FLOPs, reading $Q$ and $K$, writing $S$).
3. `max_ctx_for_memory(budget_bytes, batch, heads, bytes_per=2)`: the largest context whose attention weights for one layer fit in the budget.

## Hints

1. The weights are a `batch x heads x n_ctx x n_ctx` array.
2. For large $n$ the intensity approaches $2d/b$: 64 FLOP/byte for 64-dimensional fp16 heads.
3. Solve $B h n^2 b \le \text{budget}$ for $n$ and round down.

# Splitting attention by heads

Attention heads are independent until the output projection, so tensor parallelism gives each rank whole heads: the columns of $W_Q, W_K, W_V$ belonging to its heads, and the matching rows of $W_O$. `attention(x, Wq, Wk, Wv, Wo, heads)` is a dense reference.

1. `shard_attention(Wq, Wk, Wv, Wo, heads, tp)`: for each of `tp` ranks, its slices `(Wq_r, Wk_r, Wv_r, Wo_r)`.
2. `tp_attention(x, shards, heads_per_rank)`: run each rank's heads with its slices, and sum the partial outputs (the all-reduce).

## Hints

1. Head $h$ uses columns $h \cdot d_h$ to $(h + 1) d_h$, with $d_h = d / \text{heads}$; rank $r$ has heads $r \cdot \text{heads}/t$ to $(r+1) \cdot \text{heads}/t - 1$, a contiguous block.
2. $W_O$ is split by rows, matching the columns of the concatenated head outputs.
3. This is why the number of heads must be divisible by the tensor-parallel degree.

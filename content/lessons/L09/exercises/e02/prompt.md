# One attention head

Your softmax is provided.

1. `causal_mask(n)`: a boolean `(n, n)` array, `True` where key `j` comes after query `i`.
2. `attention(Q, K, V, causal=True, scale=True)`: scores $QK^\top$, divided by $\sqrt{d_k}$ if `scale`, masked to `-inf` where the causal mask is `True` if `causal`, softmax by rows, then the weighted sum of `V`. Return `(O, P)`.

## Hints

1. `np.triu(np.ones((n, n), dtype=bool), k=1)` is `True` strictly above the diagonal.
2. `np.where(mask, -np.inf, S)` applies the mask.
3. The first row of a causal `P` is always `(1, 0, ..., 0)`.

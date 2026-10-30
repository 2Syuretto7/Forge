# A low-rank update, as in LoRA

Fine-tuning changes a weight matrix $W$ ($d_{out} \times d_{in}$) by $\Delta$. LoRA restricts $\Delta = BA$ with $B$ of shape $(d_{out}, r)$ and $A$ of shape $(r, d_{in})$.

- `lora_params(d_out, d_in, r)`: the number of trainable numbers, $r(d_{out} + d_{in})$.
- `best_rank_r(delta, r)`: the factors `(B, A)` of the best rank-$r$ approximation of a given update, from its truncated SVD (put $\sqrt{\sigma_i}$ into each factor).
- `captured(delta, r)`: the fraction of $\|\Delta\|_F^2$ that the best rank-$r$ update keeps.

`make_update(seed=0)` in the starter gives a $256 \times 256$ update with a quickly decaying spectrum, like those measured on real fine-tuning runs.

## Hints

1. `U, s, Vt = np.linalg.svd(delta)`.
2. `B = U[:, :r] * np.sqrt(s[:r])` and `A = np.sqrt(s[:r])[:, None] * Vt[:r]`.
3. `np.sum(s[:r]**2) / np.sum(s**2)`.

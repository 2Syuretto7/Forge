# FlashAttention, backward

The forward pass is provided. Implement `flash_backward(dO, Q, K, V, O, L, Bc=4)`: loop over key blocks, recompute each block of probabilities from the stored log-sum-exp, $P = e^{cQK_j^\top - L}$, and accumulate
$$
\text{d}V_j = P^\top \text{d}O, \quad \text{d}P = \text{d}O\, V_j^\top, \quad \text{d}S = c\, P \odot (\text{d}P - D), \quad \text{d}Q \mathrel{+}= \text{d}S\, K_j, \quad \text{d}K_j = \text{d}S^\top Q,
$$
with $D_i = \sum_k \text{d}O_{ik} O_{ik}$. Return `(dQ, dK, dV)`.

## Hints

1. $D$ replaces L09's $\operatorname{rowsum}(\text{d}P \odot P)$: the two are equal because $O = PV$.
2. `P = np.exp(Q @ K_j.T * c - L[:, None])` gives the exact probabilities without renormalizing.
3. Each key block's `dK` and `dV` are complete after its iteration; `dQ` accumulates over all blocks.

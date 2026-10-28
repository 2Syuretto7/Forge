# FlashAttention, forward

`reference_attention(Q, K, V)` (non-causal, scaled) is provided. Implement `flash_attention(Q, K, V, Br=4, Bc=4)` exactly as the derivation describes: for each block of `Br` queries, loop over blocks of `Bc` keys and values, keeping per query a running maximum `m`, a running sum `l` and an output accumulator, rescaled by $\alpha = e^{m - m'}$ whenever the maximum grows. Never build the full $N \times N$ score matrix. Return `(O, L)`, where `L[i] = m + log(l)` is row $i$'s log-sum-exp of scores.

## Hints

1. Initialize `m` to $-\infty$, `l` and the accumulator to zeros, per query block.
2. Inside the loop: `s = q @ K_j.T * c`, `m_new = max(m, s.max(1))`, `p = exp(s - m_new)`, `alpha = exp(m - m_new)`.
3. `l = l * alpha + p.sum(1)` and `acc = acc * alpha[:, None] + p @ V_j`.

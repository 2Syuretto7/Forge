# Generation with a KV cache

`logits_full(ids)` is a one-layer attention model (embeddings `E`, positions `P`, projections `Wq, Wk, Wv, Wo`) that recomputes everything for a whole sequence.

1. `generate_uncached(prompt, n)`: greedy generation, recomputing the full sequence at every step.
2. `generate_cached(prompt, n)`: process the prompt once, keeping the keys and values; then for each new token compute only its query, key and value, append to the cache and attend over it. It must return exactly the same tokens.

## Hints

1. The residual stream at position $t$ is $x_t + \text{attention}_t W_o$ with $x_t = E[\text{token}] + P[t]$, and the logits are that times $E^\top$.
2. The new token's position is the length of the sequence before it was appended.
3. The cached version does work proportional to the sequence length per step; the uncached one, to its square.

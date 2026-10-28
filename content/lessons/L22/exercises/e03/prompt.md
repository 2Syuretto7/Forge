# Attention with a cache

`full_attention(Q, K, V)` recomputes causal attention over a whole sequence. Implement `cached_attention(q, k, v, cache)` for one new position: append this position's key and value to `cache["K"]` and `cache["V"]`, then attend from its query over everything cached.

Run over a sequence one position at a time, it must reproduce every row of `full_attention`.

## Hints

1. The cache already holds exactly the positions the causal mask allows, so no mask is needed.
2. Scale the scores by $1/\sqrt{d}$.
3. Each new step costs time proportional to the sequence so far, instead of recomputing the whole prefix.

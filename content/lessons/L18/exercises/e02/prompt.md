# The KV cache

Decoding reuses each earlier token's keys and values, so they are stored: per token, a key and a value for every layer and every key-value head.

1. `kv_bytes_per_token(layers, kv_heads, head_dim, bytes_per=2)`.
2. `max_batch(capacity, weight_bytes, layers, kv_heads, head_dim, tokens, bytes_per=2)`: the most sequences of `tokens` tokens whose caches fit next to the weights.

## Hints

1. $2 \times \text{layers} \times \text{kv\_heads} \times \text{head\_dim} \times \text{bytes}$.
2. Grouped-query attention shares each key-value head among several query heads, dividing the cache by that factor.
3. The cache, not the weights, is what limits the batch at long contexts.

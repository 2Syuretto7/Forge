# The serving stage: memory and step time

Before serving, size the server (L18).

1. `kv_bytes(layers, kv_heads, head_dim, tokens, bytes_per=2)`: the key-value cache for `tokens` tokens.
2. `max_sequences(memory, weight_bytes, layers, kv_heads, head_dim, ctx, bytes_per=2, reserve=0.1)`: how many full-length sequences fit after the weights and a reserved fraction of memory.
3. `decode_step_ms(weight_bytes, cache_bytes, bandwidth)`: the memory-bound time of one decode step.

## Hints

1. Two tensors (keys and values) per layer, each `kv_heads * head_dim` numbers per token.
2. Round the number of sequences down, and never below zero.
3. The capstone model is tiny: its weights and caches fit many times over, and the step time is set by kernel launches, not bytes.

def kv_bytes_per_token(layers, kv_heads, head_dim, bytes_per=2):
    """A key and a value per layer and per key-value head."""
    return 2 * layers * kv_heads * head_dim * bytes_per


def max_batch(capacity, weight_bytes, layers, kv_heads, head_dim, tokens, bytes_per=2):
    """The most sequences of `tokens` tokens whose caches fit next to the weights (rounded down,
    at least 0)."""
    free = capacity - weight_bytes
    per_seq = kv_bytes_per_token(layers, kv_heads, head_dim, bytes_per) * tokens
    return max(0, int(free // per_seq))

import math


def kv_bytes(layers, kv_heads, head_dim, tokens, bytes_per=2):
    """Bytes of keys and values cached for `tokens` tokens."""
    raise NotImplementedError


def max_sequences(memory, weight_bytes, layers, kv_heads, head_dim, ctx, bytes_per=2, reserve=0.1):
    """Full-length sequences whose caches fit in memory after the weights and a reserved
    fraction of memory for activations."""
    raise NotImplementedError


def decode_step_ms(weight_bytes, cache_bytes, bandwidth):
    """Memory-bound time of one decode step that reads the weights and the caches once."""
    raise NotImplementedError

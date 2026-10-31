def decode_intensity(n_params, batch, kv_bytes, weight_bytes=2):
    """FLOPs per byte of one decode step: 2 n_params FLOPs per sequence in the batch, against
    reading every weight once (n_params * weight_bytes) plus the KV cache (kv_bytes)."""
    return 2 * n_params * batch / (n_params * weight_bytes + kv_bytes)


def prefill_intensity(n_params, prompt_tokens, weight_bytes=2):
    """FLOPs per byte of processing a whole prompt at once: 2 n_params per token, weights read once
    (ignoring the cache, which prefill writes)."""
    return 2 * n_params * prompt_tokens / (n_params * weight_bytes)


def step_time(flops, bytes_moved, peak_flops, bandwidth):
    """Roofline time of a step: the slower of compute and memory traffic."""
    return max(flops / peak_flops, bytes_moved / bandwidth)

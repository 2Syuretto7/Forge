def model_state_bytes(n_params, zero=0, dp=1):
    """Mixed-precision Adam: 2 bytes of 16-bit weights, 2 of 16-bit gradients and 12 of fp32 master
    weights, momentum and variance per parameter. ZeRO stage k shards the first k of (optimizer
    states, gradients, weights) over the dp data-parallel ranks. Return a dict with the bytes of
    "weights", "grads" and "optim" on one GPU."""
    return {
        "weights": 2 * n_params / (dp if zero >= 3 else 1),
        "grads": 2 * n_params / (dp if zero >= 2 else 1),
        "optim": 12 * n_params / (dp if zero >= 1 else 1),
    }


def activation_bytes(seq, batch, d, heads, layers, tp=1, flash=False, checkpoint=False):
    """Activations stored for backward in 16-bit training: s b d (34 + 5 a s / d) bytes per layer
    (Korthikanti et al.), divided by tp under tensor and sequence parallelism; FlashAttention drops
    the 5 a s / d term. With full checkpointing only each layer's 2 s b d byte input is kept, plus
    one layer's activations while it is recomputed."""
    per_layer = seq * batch * d * (34 + (0 if flash else 5 * heads * seq / d)) / tp
    if checkpoint:
        return layers * 2 * seq * batch * d / tp + per_layer
    return layers * per_layer

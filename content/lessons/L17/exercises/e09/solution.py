def bytes_per_param(optimizer="adam", mixed=True):
    """Training memory per parameter, without activations. Mixed precision with Adam: fp16 weights
    and gradients (2 + 2) plus fp32 master weights, first and second moments (4 + 4 + 4). Plain fp32
    with Adam: weights, gradients and two moments in fp32. SGD without momentum keeps no moments."""
    if optimizer == "adam":
        return (2 + 2 + 4 + 4 + 4) if mixed else (4 + 4 + 4 + 4)
    return (2 + 2 + 4) if mixed else (4 + 4)


def training_memory_gb(n_params, optimizer="adam", mixed=True):
    return n_params * bytes_per_param(optimizer, mixed) / 1e9


def inference_memory_gb(n_params, bytes_per_weight=2):
    """Weights only, in the serving precision."""
    return n_params * bytes_per_weight / 1e9

def matvec(W, x):
    """Multiply list-of-rows W by list x with loops; return (y, flops)."""
    raise NotImplementedError


def mlp_flops(widths, batch=1):
    """Forward-pass FLOPs of dense layers with these widths, for batch inputs."""
    raise NotImplementedError


def mlp_params(widths):
    """Weights plus biases of dense layers with these widths."""
    raise NotImplementedError


def train_flops(n_params, n_tokens):
    """About 6 N D FLOPs to train N parameters on D tokens."""
    raise NotImplementedError

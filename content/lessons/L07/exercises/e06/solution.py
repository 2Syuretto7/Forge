import numpy as np


def matmul_backward(dY, X, W):
    """Y = X W. Return (dX, dW)."""
    return dY @ W.T, X.T @ dY


def step_flops(batch_tokens, layer_shapes):
    """FLOPs of one training step through linear layers of the given (n_in, n_out) shapes:
    forward 2 * tokens * n_in * n_out per layer, backward twice that."""
    fwd = sum(2 * batch_tokens * a * b for a, b in layer_shapes)
    return 3 * fwd


def flops_per_token_per_param():
    """The rule of thumb that follows: training costs about this many FLOPs per token per parameter."""
    return 6

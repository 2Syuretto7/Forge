import numpy as np


def matmul_backward(dY, X, W):
    """Y = X W. Return (dX, dW)."""
    raise NotImplementedError


def step_flops(batch_tokens, layer_shapes):
    """FLOPs of one training step through linear layers of the given (n_in, n_out) shapes:
    forward 2 * tokens * n_in * n_out per layer, backward twice that."""
    raise NotImplementedError


def flops_per_token_per_param():
    """The rule of thumb that follows: training costs about this many FLOPs per token per parameter."""
    raise NotImplementedError

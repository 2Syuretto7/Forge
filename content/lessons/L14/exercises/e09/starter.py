import numpy as np


def forward(x, Ws):
    """h_{i+1} = tanh(h_i W_i), with h_0 = x. Return the list of all activations h_0 .. h_L."""
    raise NotImplementedError


def backward(hs, Ws, dout):
    """Gradients of the loss with respect to each W, given dL/dh_L = dout and all activations."""
    raise NotImplementedError


def checkpointed_grads(x, Ws, dout, k):
    """Keep only every k-th activation (h_0, h_k, h_2k, ...) in the forward pass. In backward,
    recompute each segment's activations from its checkpoint, then backpropagate through it.
    Return (grads, peak number of activations stored at once, counting checkpoints and one
    recomputed segment)."""
    raise NotImplementedError

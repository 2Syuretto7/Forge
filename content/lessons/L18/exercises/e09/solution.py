import numpy as np


def forward(x, Ws):
    """h_{i+1} = tanh(h_i W_i), with h_0 = x. Return the list of all activations h_0 .. h_L."""
    hs = [x]
    for W in Ws:
        hs.append(np.tanh(hs[-1] @ W))
    return hs


def backward(hs, Ws, dout):
    """Gradients of the loss with respect to each W, given dL/dh_L = dout and all activations."""
    grads = [None] * len(Ws)
    g = dout
    for i in reversed(range(len(Ws))):
        dz = g * (1 - hs[i + 1] ** 2)
        grads[i] = hs[i].T @ dz
        g = dz @ Ws[i].T
    return grads


def checkpointed_grads(x, Ws, dout, k):
    """Keep only every k-th activation (h_0, h_k, h_2k, ...) in the forward pass. In backward,
    recompute each segment's activations from its checkpoint, then backpropagate through it.
    Return (grads, peak number of activations stored at once, counting checkpoints and one
    recomputed segment)."""
    L = len(Ws)
    h = x
    checkpoints = {0: x}
    for i, W in enumerate(Ws):
        h = np.tanh(h @ W)
        if (i + 1) % k == 0 and i + 1 < L:
            checkpoints[i + 1] = h
    grads = [None] * L
    g = dout
    peak = 0
    starts = sorted(checkpoints)
    for idx in reversed(range(len(starts))):
        a = starts[idx]
        b = starts[idx + 1] if idx + 1 < len(starts) else L
        seg = forward(checkpoints[a], Ws[a:b])
        peak = max(peak, len(checkpoints) + len(seg) - 1)
        for i in reversed(range(a, b)):
            dz = g * (1 - seg[i - a + 1] ** 2)
            grads[i] = seg[i - a].T @ dz
            g = dz @ Ws[i].T
    return grads, peak

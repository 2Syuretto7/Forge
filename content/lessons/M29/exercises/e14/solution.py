import numpy as np


def first_step(b1, b2, lr=1.0):
    """Length of the uncorrected first Adam step per coordinate."""
    return lr * (1 - b1) / np.sqrt(1 - b2)


def step_lengths(g, lr, iters, b1=0.9, b2=0.999, bias_correction=True):
    """Per-step moves under a constant gradient."""
    m = v = 0.0
    out = []
    for t in range(1, iters + 1):
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mh, vh = (m / (1 - b1**t), v / (1 - b2**t)) if bias_correction else (m, v)
        out.append(lr * mh / (np.sqrt(vh) + 1e-12))
    return np.array(out)

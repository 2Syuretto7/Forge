import numpy as np


def adam_step(x, g, state, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8):
    """One Adam update with bias correction."""
    state["t"] += 1
    state["m"] = b1 * state["m"] + (1 - b1) * g
    state["v"] = b2 * state["v"] + (1 - b2) * g * g
    mh = state["m"] / (1 - b1 ** state["t"])
    vh = state["v"] / (1 - b2 ** state["t"])
    return x - lr * mh / (np.sqrt(vh) + eps)


def first_step_size(g, lr):
    """Size of the first Adam update."""
    state = {"m": np.zeros_like(g), "v": np.zeros_like(g), "t": 0}
    return np.abs(adam_step(np.zeros_like(g), g, state, lr) )

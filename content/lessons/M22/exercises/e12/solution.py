import numpy as np


def layer_second_moments(depth, width, scale, activation="linear", batch=500, seed=0):
    """Mean squared activation after each of depth random layers."""
    rng = np.random.default_rng(seed)
    h = rng.standard_normal((batch, width))
    out = []
    for _ in range(depth):
        W = rng.standard_normal((width, width)) * (scale / np.sqrt(width))
        h = h @ W
        if activation == "relu":
            h = np.maximum(h, 0)
        out.append(float(np.mean(h * h)))
    return out


def preserving_scale(activation):
    """Scale that keeps the second moment constant."""
    return float(np.sqrt(2.0)) if activation == "relu" else 1.0


def predicted_factor(scale, activation, depth):
    """Predicted growth of the second moment over depth layers."""
    per = scale**2 / (2 if activation == "relu" else 1)
    return per**depth

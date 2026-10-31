import numpy as np


def forward_second_moments(L, width, c, rng, batch=64):
    """Mean square of activations after each of L ReLU layers."""
    x = rng.standard_normal((batch, width))
    out = []
    for _ in range(L):
        W = rng.standard_normal((width, width)) * np.sqrt(2 * c / width)
        x = np.maximum(x @ W, 0)
        out.append(float(np.mean(x**2)))
    return out


def predicted_ratio(c, L):
    """Growth of the second moment over L layers."""
    return c**L

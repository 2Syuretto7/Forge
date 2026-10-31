import numpy as np


def activation_rms(depth, width, std, seed=0, batch=64):
    rng = np.random.default_rng(seed)
    h = rng.normal(size=(batch, width))
    out = []
    for _ in range(depth):
        W = rng.normal(size=(width, width)) * std
        h = np.maximum(h @ W, 0)
        out.append(float(np.sqrt(np.mean(h ** 2))))
    return out


def predicted_growth(width, std):
    return std * np.sqrt(width / 2)

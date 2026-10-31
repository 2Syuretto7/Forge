import numpy as np


def residual_rms(depth, alpha, branch="linear", width=256, batch=256, seed=0):
    """h <- h + alpha * F(h) with fresh weights per layer, from unit-normal h, where F(h) = h W with
    W ~ N(0, 1/width) ("linear") or relu(h W) with He-initialized W ("relu").
    Return the RMS of h before the first layer and after each layer (depth + 1 numbers)."""
    rng = np.random.default_rng(seed)
    h = rng.normal(size=(batch, width))
    out = [float(np.sqrt(np.mean(h * h)))]
    for _ in range(depth):
        if branch == "linear":
            h = h + alpha * (h @ (rng.normal(size=(width, width)) * np.sqrt(1.0 / width)))
        else:
            h = h + alpha * np.maximum(h @ (rng.normal(size=(width, width)) * np.sqrt(2.0 / width)), 0.0)
        out.append(float(np.sqrt(np.mean(h * h))))
    return out


def predicted_growth(depth, alpha):
    """RMS(h_depth) / RMS(h_0) when each layer multiplies the second moment by 1 + alpha^2."""
    return (1.0 + alpha ** 2) ** (depth / 2)

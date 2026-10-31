import numpy as np


def adam(grad, x0, lr, iters, b1=0.9, b2=0.999, eps=1e-8, bias_correction=True):
    """Iterates of Adam."""
    x = np.array(x0, dtype=float)
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    out = [x.copy()]
    for t in range(1, iters + 1):
        g = grad(x)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mh, vh = (m / (1 - b1**t), v / (1 - b2**t)) if bias_correction else (m, v)
        x = x - lr * mh / (np.sqrt(vh) + eps)
        out.append(x.copy())
    return out


def adam_moments(gs, b1=0.9, b2=0.999):
    """Bias-corrected first and second moments of a gradient sequence."""
    m = v = 0.0
    mh, vh = [], []
    for t, g in enumerate(gs, start=1):
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mh.append(m / (1 - b1**t))
        vh.append(v / (1 - b2**t))
    return np.array(mh), np.array(vh)

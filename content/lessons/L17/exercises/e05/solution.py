import numpy as np


def underflow_fraction(grads, scale=1.0):
    """Fraction of the nonzero float32 gradients that become exactly 0 when (grads * scale) is cast to
    float16."""
    g = np.asarray(grads, dtype=np.float32)
    nz = g != 0
    return float(np.mean((g[nz] * np.float32(scale)).astype(np.float16) == 0))


def scaled_loss_and_grad(w, X, y, scale):
    """Loss scaling: return (scale * L, scale * dL/dw) for the least-squares loss
    L = mean((X w - y)^2) / 2. The optimizer divides by scale before using the gradient."""
    r = X @ w - y
    return scale * 0.5 * float(np.mean(r * r)), scale * (X.T @ r) / len(y)

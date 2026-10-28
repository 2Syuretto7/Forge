import numpy as np


def per_tensor_int8(W):
    """One scale for the whole matrix (largest absolute value / 127); return dequantized weights."""
    s = np.abs(W).max() / 127
    return np.clip(np.round(W / s), -127, 127) * s


def mixed_precision_int8(W, X, k):
    """LLM.int8-style: the k input features (columns of W) with the largest typical activation
    magnitude in X (mean absolute value over the rows of X) stay in full precision; the other
    columns are quantized per output row. Return the effective weights."""
    keep = np.argsort(np.abs(X).mean(axis=0))[-k:]
    rest = np.setdiff1d(np.arange(W.shape[1]), keep)
    out = W.astype(float).copy()
    sub = W[:, rest]
    s = np.abs(sub).max(axis=1, keepdims=True) / 127
    s = np.where(s == 0, 1.0, s)
    out[:, rest] = np.clip(np.round(sub / s), -127, 127) * s
    return out

import numpy as np


def output_error(W_hat, W, X):
    """The mean squared error of the layer's outputs, |X W^T - X W_hat^T|^2 / n over the n rows of
    calibration inputs X, and its gradient with respect to W_hat."""
    D = X @ (W - W_hat).T
    n = X.shape[0]
    return float(np.sum(D ** 2) / n), -2 * D.T @ X / n


def group_quantize(W, bits, group):
    """Symmetric quantization with one scale per `group` consecutive weights in each row; returns
    the dequantized weights."""
    levels = 2 ** (bits - 1) - 1
    out = np.empty_like(W, dtype=float)
    for j in range(0, W.shape[1], group):
        blk = W[:, j:j + group]
        s = np.abs(blk).max(axis=1, keepdims=True) / levels
        s = np.where(s == 0, 1.0, s)
        out[:, j:j + group] = np.clip(np.round(blk / s), -levels, levels) * s
    return out

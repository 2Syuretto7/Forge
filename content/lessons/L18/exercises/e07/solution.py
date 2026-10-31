import numpy as np


def quantize_int8(W):
    """Symmetric per-output-channel quantization: each row's scale is its largest absolute value
    divided by 127; values round to the nearest integer in [-127, 127]. Return (int8 array,
    scales)."""
    scale = np.abs(W).max(axis=1, keepdims=True) / 127
    scale = np.where(scale == 0, 1.0, scale)
    q = np.clip(np.round(W / scale), -127, 127).astype(np.int8)
    return q, scale[:, 0]


def dequantize(q, scale):
    return q.astype(np.float64) * scale[:, None]


def int8_matmul(x, q, scale):
    """x W^T with the int8 weights: multiply by the integers, then scale each output column."""
    return (x @ q.astype(np.float64).T) * scale[None, :]

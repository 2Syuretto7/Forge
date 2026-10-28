import numpy as np


def quantize_int8(W):
    """Symmetric per-output-channel quantization: each row's scale is its largest absolute value
    divided by 127; values round to the nearest integer in [-127, 127]. Return (int8 array,
    scales)."""
    raise NotImplementedError


def dequantize(q, scale):
    raise NotImplementedError


def int8_matmul(x, q, scale):
    """x W^T with the int8 weights: multiply by the integers, then scale each output column."""
    raise NotImplementedError

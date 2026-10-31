import numpy as np


def per_tensor_int8(W):
    """One scale for the whole matrix (largest absolute value / 127); return dequantized weights."""
    raise NotImplementedError


def mixed_precision_int8(W, X, k):
    """LLM.int8-style: the k input features (columns of W) with the largest typical activation
    magnitude in X (mean absolute value over the rows of X) stay in full precision; the other
    columns are quantized per output row. Return the effective weights."""
    raise NotImplementedError

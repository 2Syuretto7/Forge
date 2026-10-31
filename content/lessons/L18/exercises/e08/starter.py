import numpy as np


def output_error(W_hat, W, X):
    """The mean squared error of the layer's outputs, |X W^T - X W_hat^T|^2 / n over the n rows of
    calibration inputs X, and its gradient with respect to W_hat."""
    raise NotImplementedError


def group_quantize(W, bits, group):
    """Symmetric quantization with one scale per `group` consecutive weights in each row; returns
    the dequantized weights."""
    raise NotImplementedError

import numpy as np


def residual_rms(depth, alpha, branch="linear", width=256, batch=256, seed=0):
    """h <- h + alpha * F(h) with fresh weights per layer, from unit-normal h, where F(h) = h W with
    W ~ N(0, 1/width) ("linear") or relu(h W) with He-initialized W ("relu").
    Return the RMS of h before the first layer and after each layer (depth + 1 numbers)."""
    raise NotImplementedError


def predicted_growth(depth, alpha):
    """RMS(h_depth) / RMS(h_0) when each layer multiplies the second moment by 1 + alpha^2."""
    raise NotImplementedError

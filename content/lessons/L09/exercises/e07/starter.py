import numpy as np


def rope(X, positions, base=10000.0):
    """Rotate each pair of features (2i, 2i+1) of row p by the angle p * theta_i, with
    theta_i = base^(-2i/d). X has shape (n, d) with d even; positions has shape (n,)."""
    raise NotImplementedError

import numpy as np


def lora_params(k, d, r):
    """Trainable parameters of a rank-r LoRA update."""
    raise NotImplementedError


def full_params(k, d):
    """Parameters of the full matrix."""
    raise NotImplementedError


def fraction(k, d, r):
    """LoRA parameters as a fraction of the full matrix."""
    raise NotImplementedError


def merged(W0, B, A):
    """W0 + B A."""
    raise NotImplementedError


def rank_of(M, tol=1e-9):
    """Numerical rank."""
    raise NotImplementedError

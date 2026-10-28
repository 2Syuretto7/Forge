import numpy as np


def merge(W0, A, B, alpha):
    """The single weight matrix equivalent to the LoRA layer: W0 + (alpha / r) B A."""
    raise NotImplementedError


def lora_params(d_in, d_out, r):
    """Trainable parameters of a rank-r adapter on a d_out x d_in matrix."""
    raise NotImplementedError


def trainable_fraction(n_layer, d, r, per_layer=("q", "v")):
    """Fraction of a transformer's 12 n_layer d^2 block parameters that rank-r adapters on the
    listed d x d projections of every layer train."""
    raise NotImplementedError

import numpy as np


def forward_second_moments(L, width, c, rng, batch=64):
    """Mean square of activations after each of L ReLU layers."""
    raise NotImplementedError


def predicted_ratio(c, L):
    """Growth of the second moment over L layers."""
    raise NotImplementedError

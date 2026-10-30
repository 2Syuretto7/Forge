import numpy as np


def linear(x, W, b):
    """x W^T + b."""
    raise NotImplementedError


def wrong_runs(d_in, d_out):
    """Whether x @ W + b runs for these sizes."""
    raise NotImplementedError


def detect_transpose_bug(f, d=4, seed=0):
    """True if f disagrees with a correct linear layer on random square inputs."""
    raise NotImplementedError

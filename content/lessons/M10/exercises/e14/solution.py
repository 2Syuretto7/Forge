import numpy as np


def linear(x, W, b):
    """x W^T + b."""
    return x @ W.T + b


def wrong_runs(d_in, d_out):
    """Whether x @ W + b runs for these sizes."""
    return d_in == d_out


def detect_transpose_bug(f, d=4, seed=0):
    """True if f disagrees with a correct linear layer on random square inputs."""
    rng = np.random.default_rng(seed)
    x, W, b = rng.normal(size=(5, d)), rng.normal(size=(d, d)), rng.normal(size=d)
    return not np.allclose(f(x, W, b), linear(x, W, b))

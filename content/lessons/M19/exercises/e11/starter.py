import time

import numpy as np


# provided
def make_net(n, width=32, depth=20, seed=0):
    rng = np.random.default_rng(seed)
    Ws = [rng.normal(size=(width, n)) / np.sqrt(n)] + [rng.normal(size=(width, width)) / np.sqrt(width) for _ in range(depth - 1)]
    return Ws, rng.normal(size=width)


def forward_mode_grad(Ws, w, x):
    """All n JVPs at once through a tangent matrix."""
    raise NotImplementedError


def reverse_mode_grad(Ws, w, x):
    """One forward pass, one backward pass of VJPs."""
    raise NotImplementedError


def time_ratio(n, reps=5):
    """Forward-mode time over reverse-mode time."""
    raise NotImplementedError

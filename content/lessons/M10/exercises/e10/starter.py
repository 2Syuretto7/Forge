import time

import numpy as np


def batched_loop(A, B):
    """Pair by pair in a Python loop."""
    raise NotImplementedError


def batched(A, B):
    """One batched call."""
    raise NotImplementedError


def measure(b, n, seed=0):
    """(flops, seconds, flops per second) for a batch of b products of size n."""
    raise NotImplementedError

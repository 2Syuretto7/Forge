import time

import numpy as np


def time_matmul(n, min_time=0.02):
    """Seconds per n x n matrix product, timing batches that double until min_time."""
    raise NotImplementedError


def flops_per_second(n):
    """Measured FLOP/s of an n x n matrix product."""
    raise NotImplementedError


def predict_seconds(n, rate):
    """Predicted seconds for an n x n product at rate FLOP/s."""
    raise NotImplementedError

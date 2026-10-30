import math


def activation_bytes(depth, width, batch):
    """Stored activations, float32."""
    raise NotImplementedError


def checkpoint_bytes(depth, width, batch, k):
    """Memory with a checkpoint every k layers."""
    raise NotImplementedError


def best_k(depth):
    """k minimizing ceil(depth / k) + k."""
    raise NotImplementedError


def extra_compute(k):
    """Extra forward passes from recomputation."""
    raise NotImplementedError

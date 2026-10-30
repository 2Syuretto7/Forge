import math


def activation_bytes(depth, width, batch):
    """Stored activations, float32."""
    return 4 * depth * width * batch


def checkpoint_bytes(depth, width, batch, k):
    """Memory with a checkpoint every k layers."""
    return 4 * (math.ceil(depth / k) + k) * width * batch


def best_k(depth):
    """k minimizing ceil(depth / k) + k."""
    return min(range(1, depth + 1), key=lambda k: (math.ceil(depth / k) + k, k))


def extra_compute(k):
    """Extra forward passes from recomputation."""
    return 0.0 if k == 1 else 1.0

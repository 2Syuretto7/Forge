import numpy as np


def global_norm(grads):
    """The L2 norm of all gradient arrays taken together."""
    return float(np.sqrt(sum(np.sum(g * g) for g in grads)))


def clip_by_global_norm(grads, max_norm):
    """Scale every gradient by min(1, max_norm / norm) so the global norm is at most max_norm.
    Return (clipped grads, the norm before clipping)."""
    norm = global_norm(grads)
    scale = min(1.0, max_norm / norm) if norm > 0 else 1.0
    return [g * scale for g in grads], norm

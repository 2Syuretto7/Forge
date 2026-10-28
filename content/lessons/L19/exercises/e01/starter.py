import numpy as np


def global_norm(grads):
    """The L2 norm of all gradient arrays taken together."""
    raise NotImplementedError


def clip_by_global_norm(grads, max_norm):
    """Scale every gradient by min(1, max_norm / norm) so the global norm is at most max_norm.
    Return (clipped grads, the norm before clipping)."""
    raise NotImplementedError

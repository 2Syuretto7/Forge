import numpy as np


def smoothed_xent(logits, y, eps):
    """Cross-entropy against the smoothed target (1 - eps) onehot(y) + eps / V, mean over the batch,
    and its gradient w.r.t. the logits."""
    raise NotImplementedError

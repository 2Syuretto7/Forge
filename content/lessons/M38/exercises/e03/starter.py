import numpy as np


def log_softmax(z):
    """Stable log-softmax."""
    raise NotImplementedError


def _h(z, ref_logp, beta):
    raise NotImplementedError


def dpo_loss(z, ref_logp, N, beta):
    """Mean DPO loss over the comparisons counted in N."""
    raise NotImplementedError


def grad_dpo_loss(z, ref_logp, N, beta):
    """Gradient of the DPO loss in the logits."""
    raise NotImplementedError

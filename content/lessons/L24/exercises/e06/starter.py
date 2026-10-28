import numpy as np


def log_softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    return z - np.log(np.exp(z).sum(axis=1, keepdims=True))


def group_advantages(rewards, eps=1e-6):
    """Rewards (groups, k): each reward minus its group's mean, divided by the group's standard
    deviation plus eps."""
    raise NotImplementedError


def pg_loss(logits, actions, adv, ref_logits, beta):
    """Policy-gradient loss with a KL penalty for n sampled actions from policies given by
    logits (n, V). With u = log pi_ref(a) - log pi(a), the loss is
    mean(-adv * log pi(a) + beta * (exp(u) - 1 - u)). Return (loss, dlogits)."""
    raise NotImplementedError

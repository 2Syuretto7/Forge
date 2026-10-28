import numpy as np


def log_softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    return z - np.log(np.exp(z).sum(axis=1, keepdims=True))


def group_advantages(rewards, eps=1e-6):
    """Rewards (groups, k): each reward minus its group's mean, divided by the group's standard
    deviation plus eps."""
    r = np.asarray(rewards, dtype=float)
    return (r - r.mean(axis=1, keepdims=True)) / (r.std(axis=1, keepdims=True) + eps)


def pg_loss(logits, actions, adv, ref_logits, beta):
    """Policy-gradient loss with a KL penalty for n sampled actions from policies given by
    logits (n, V). With u = log pi_ref(a) - log pi(a), the loss is
    mean(-adv * log pi(a) + beta * (exp(u) - 1 - u)). Return (loss, dlogits)."""
    n = len(actions)
    lp = log_softmax(logits)
    rows = np.arange(n)
    lpa = lp[rows, actions]
    u = log_softmax(ref_logits)[rows, actions] - lpa
    loss = np.mean(-adv * lpa + beta * (np.exp(u) - 1 - u))
    coef = (-adv + beta * (1 - np.exp(u))) / n
    onehot = np.zeros_like(logits)
    onehot[rows, actions] = 1
    return float(loss), coef[:, None] * (onehot - np.exp(lp))

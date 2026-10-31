import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def rl_arithmetic(steps, lr, group, seed, beta=0.0, theta0=None):
    """A policy answering "a + b mod 10" for digits a, b: logits theta[a, b, :] over the answer
    digit. Each step, for every one of the 100 prompts, sample `group` answers, reward 1 for the
    right digit, compute group advantages (mean-centred, std-normalized with 1e-6), and ascend
    sum (adv * score) / group, minus beta times the gradient of KL(pi || pi0) where pi0 is the
    initial policy. Return (final theta, accuracy of the greedy answers)."""
    raise NotImplementedError

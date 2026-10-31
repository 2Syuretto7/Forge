import numpy as np


def softmax(z, T=1.0):
    z = z / T
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def distill_loss(student, teacher, labels, T, alpha):
    """alpha T^2 KL(softmax(teacher / T) || softmax(student / T)) + (1 - alpha) CE(student, labels),
    each averaged over rows. Return (loss, gradient with respect to the student logits)."""
    n = len(labels)
    pt, ps = softmax(teacher, T), softmax(student, T)
    kl = np.sum(pt * (np.log(pt) - np.log(ps)), axis=1).mean()
    p = softmax(student)
    ce = -np.log(p[np.arange(n), labels]).mean()
    g_ce = p.copy()
    g_ce[np.arange(n), labels] -= 1
    grad = alpha * T * (ps - pt) / n + (1 - alpha) * g_ce / n
    return alpha * T * T * kl + (1 - alpha) * ce, grad

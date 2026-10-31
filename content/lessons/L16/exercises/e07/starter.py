import numpy as np


def softmax(z, T=1.0):
    raise NotImplementedError


def distill_loss(student, teacher, labels, T, alpha):
    """alpha T^2 KL(softmax(teacher / T) || softmax(student / T)) + (1 - alpha) CE(student, labels),
    each averaged over rows. Return (loss, gradient with respect to the student logits)."""
    raise NotImplementedError

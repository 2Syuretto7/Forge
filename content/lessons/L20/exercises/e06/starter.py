import numpy as np


def fit_lora(target, r, alpha, steps=3000, lr=0.05, seed=0):
    """Fit (alpha / r) B A to the target update by gradient descent on 0.5 |(alpha / r) B A - target|^2,
    starting from B = 0 and A with entries N(0, 1/r) as LoRA does. Return (A, B, final loss)."""
    raise NotImplementedError

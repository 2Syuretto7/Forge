import numpy as np


def fit_lora(target, r, alpha, steps=3000, lr=0.05, seed=0):
    """Fit (alpha / r) B A to the target update by gradient descent on 0.5 |(alpha / r) B A - target|^2,
    starting from B = 0 and A with entries N(0, 1/r) as LoRA does. Return (A, B, final loss)."""
    rng = np.random.default_rng(seed)
    d_out, d_in = target.shape
    A = rng.normal(size=(r, d_in)) / np.sqrt(r)
    B = np.zeros((d_out, r))
    s = alpha / r
    for _ in range(steps):
        E = s * B @ A - target
        gB = s * E @ A.T
        gA = s * B.T @ E
        A -= lr * gA
        B -= lr * gB
    return A, B, 0.5 * float(np.sum((s * B @ A - target) ** 2))

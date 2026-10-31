import numpy as np


def _train(X, Y, W0, r, steps, lr=0.1, seed=0):
    rng = np.random.default_rng(seed)
    B = np.zeros((W0.shape[0], r))
    A = 0.1 * rng.standard_normal((r, W0.shape[1]))
    n = len(X)
    C, D = X.T @ X / n, X.T @ Y / n
    for _ in range(steps):
        G = C @ (W0 + B @ A) - D
        B, A = B - lr * G @ A.T, A - lr * B.T @ G
    R = X @ (W0 + B @ A) - Y
    return float(np.sum(R * R) / (2 * n))


def rank_sweep(X, Y, W0, ranks, steps=1500):
    """Loss and trainable fraction for each LoRA rank."""
    k, d = W0.shape
    return {r: (_train(X, Y, W0, r, steps), r * (k + d) / (k * d)) for r in ranks}


def full_loss(X, Y):
    """Loss of full least-squares fine-tuning."""
    W = np.linalg.lstsq(X, Y, rcond=None)[0]
    R = X @ W - Y
    return float(np.sum(R * R) / (2 * len(X)))


def smallest_rank_within(sweep, full, slack=0.05):
    """Smallest rank whose loss is within slack of full fine-tuning."""
    for r in sorted(sweep):
        if sweep[r][0] <= (1 + slack) * full:
            return r
    return None

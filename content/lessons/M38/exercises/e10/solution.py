import numpy as np


def train_loss(X, Y, W0, r, steps=1500, lr=0.1, seed=0):
    """Final loss of LoRA training at rank r."""
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


def predicted_floor(X, dW, r, noise_var):
    """Approximate best loss of a rank-r update with white inputs."""
    U, s, Vt = np.linalg.svd(dW, full_matrices=False)
    E = dW - (U[:, :r] * s[:r]) @ Vt[:r]
    return float(np.sum((X @ E) ** 2) / (2 * len(X)) + dW.shape[1] * noise_var / 2)

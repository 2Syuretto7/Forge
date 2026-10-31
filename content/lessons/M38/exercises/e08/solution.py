import numpy as np


def loss(B, A, X, Y, W0):
    """Half mean squared error of the LoRA model."""
    R = X @ (W0 + B @ A) - Y
    return float(np.sum(R * R) / (2 * len(X)))


def grads(B, A, X, Y, W0):
    """Gradients of the loss in B and A."""
    G = X.T @ (X @ (W0 + B @ A) - Y) / len(X)
    return G @ A.T, B.T @ G


def train_lora(X, Y, W0, r, steps=1500, lr=0.1, seed=0):
    """Gradient descent on the LoRA factors."""
    rng = np.random.default_rng(seed)
    B = np.zeros((W0.shape[0], r))
    A = 0.1 * rng.standard_normal((r, W0.shape[1]))
    C, D = X.T @ X / len(X), X.T @ Y / len(X)
    for _ in range(steps):
        G = C @ (W0 + B @ A) - D
        B, A = B - lr * G @ A.T, A - lr * B.T @ G
    return B, A

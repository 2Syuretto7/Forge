import numpy as np


def logistic_loss_grad(w, X, y):
    """Mean logistic loss of labels y in {0, 1} and its gradient."""
    z = X @ w
    p = 1 / (1 + np.exp(-z))
    return float(np.mean(np.logaddexp(0, z) - y * z)), X.T @ (p - y) / len(y)


def finetune(w_pre, X, y, lam, steps=500, lr=0.5):
    """Gradient descent from the pretrained weights on the new task's loss plus
    lam / 2 |w - w_pre|^2, which pulls the weights back toward where they started."""
    w = w_pre.copy()
    for _ in range(steps):
        _, g = logistic_loss_grad(w, X, y)
        w -= lr * (g + lam * (w - w_pre))
    return w

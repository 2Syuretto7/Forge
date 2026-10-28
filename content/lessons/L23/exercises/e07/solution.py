import numpy as np


def sae_loss(params, X, l1):
    """A sparse autoencoder on activations X (n, d) with m latents: z = relu((X - b_d) W_e^T + b_e),
    X_hat = z W_d + b_d, loss = mean over rows of |X - X_hat|^2 + l1 * sum(z). params = (W_e (m, d),
    b_e (m,), W_d (m, d), b_d (d,)). Return (loss, gradients in the same order)."""
    We, be, Wd, bd = params
    n = len(X)
    U = X - bd
    pre = U @ We.T + be
    z = np.maximum(pre, 0)
    Xh = z @ Wd + bd
    E = Xh - X
    loss = np.sum(E ** 2) / n + l1 * np.sum(z) / n
    dXh = 2 * E / n
    dWd = z.T @ dXh
    dz = dXh @ Wd.T + l1 / n
    dpre = dz * (pre > 0)
    dWe = dpre.T @ U
    dbe = dpre.sum(axis=0)
    dbd = dXh.sum(axis=0) - (dpre @ We).sum(axis=0)
    return float(loss), (dWe, dbe, dWd, dbd)

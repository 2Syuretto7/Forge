import numpy as np


def sae_loss(params, X, l1):
    """A sparse autoencoder on activations X (n, d) with m latents: z = relu((X - b_d) W_e^T + b_e),
    X_hat = z W_d + b_d, loss = mean over rows of |X - X_hat|^2 + l1 * sum(z). params = (W_e (m, d),
    b_e (m,), W_d (m, d), b_d (d,)). Return (loss, gradients in the same order)."""
    raise NotImplementedError

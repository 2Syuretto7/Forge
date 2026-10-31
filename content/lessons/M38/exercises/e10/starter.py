import numpy as np


def train_loss(X, Y, W0, r, steps=1500, lr=0.1, seed=0):
    """Final loss of LoRA training at rank r."""
    raise NotImplementedError


def predicted_floor(X, dW, r, noise_var):
    """Approximate best loss of a rank-r update with white inputs."""
    raise NotImplementedError

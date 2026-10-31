import numpy as np


def loss(B, A, X, Y, W0):
    """Half mean squared error of the LoRA model."""
    raise NotImplementedError


def grads(B, A, X, Y, W0):
    """Gradients of the loss in B and A."""
    raise NotImplementedError


def train_lora(X, Y, W0, r, steps=1500, lr=0.1, seed=0):
    """Gradient descent on the LoRA factors."""
    raise NotImplementedError

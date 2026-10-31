import numpy as np


def mse_grad(w, X, y):
    """L = mean((X w - y)^2) / 2 and its gradient."""
    raise NotImplementedError


def train(X, y, lr, steps, master):
    """Gradient descent where the forward and backward pass use float16 copies of w. With
    master=True, a float32 master copy receives the updates; with master=False, w itself lives in
    float16 and every update is rounded to float16. Return the final float32 loss."""
    raise NotImplementedError

import numpy as np


def forward(Ws, x):
    """[x, h1, h2, y]."""
    W1, W2, W3 = Ws
    h1 = np.tanh(W1 @ x)
    h2 = np.tanh(W2 @ h1)
    return [x, h1, h2, W3 @ h2]


def layer_jacobians(Ws, x):
    """Jacobians of the three stages."""
    W1, W2, W3 = Ws
    _, h1, h2, _ = forward(Ws, x)
    return [(1 - h1 ** 2)[:, None] * W1, (1 - h2 ** 2)[:, None] * W2, W3]


def network_jacobian(Ws, x):
    """dy/dx."""
    J1, J2, J3 = layer_jacobians(Ws, x)
    return J3 @ J2 @ J1

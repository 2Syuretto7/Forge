import numpy as np


def forward(Ws, x):
    """[x, h1, h2, y]."""
    raise NotImplementedError


def layer_jacobians(Ws, x):
    """Jacobians of the three stages."""
    raise NotImplementedError


def network_jacobian(Ws, x):
    """dy/dx."""
    raise NotImplementedError

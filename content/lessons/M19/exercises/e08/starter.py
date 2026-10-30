import numpy as np


def _stats(x, eps):
    raise NotImplementedError


def layernorm(x, eps=1e-5):
    raise NotImplementedError


def layernorm_vjp(x, u, eps=1e-5):
    raise NotImplementedError


def layernorm_jacobian(x, eps=1e-5):
    raise NotImplementedError

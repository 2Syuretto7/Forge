import numpy as np


def _stats(x, eps):
    mu = x.mean()
    sigma = np.sqrt(np.mean((x - mu) ** 2) + eps)
    return mu, sigma


def layernorm(x, eps=1e-5):
    mu, sigma = _stats(x, eps)
    return (x - mu) / sigma


def layernorm_vjp(x, u, eps=1e-5):
    _, sigma = _stats(x, eps)
    xh = layernorm(x, eps)
    return (u - u.mean() - (u * xh).mean() * xh) / sigma


def layernorm_jacobian(x, eps=1e-5):
    d = x.size
    return np.stack([layernorm_vjp(x, np.eye(d)[i], eps) for i in range(d)])

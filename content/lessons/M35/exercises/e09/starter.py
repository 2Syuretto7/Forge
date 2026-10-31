import numpy as np

N0, D0 = 1e9, 1e10


def surface(theta, N, D):
    """E + exp(a - alpha u) + exp(b - beta v)."""
    raise NotImplementedError


def grad_surface(theta, N, D):
    """Jacobian of the surface in (E, a, alpha, b, beta)."""
    raise NotImplementedError


def fit_surface(N, D, L, theta0, iters=200):
    """Levenberg-Marquardt fit of the loss surface."""
    raise NotImplementedError


def to_chinchilla(theta):
    """(E, A, alpha, B, beta) in the original parametrization."""
    raise NotImplementedError

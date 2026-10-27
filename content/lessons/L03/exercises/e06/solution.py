import numpy as np


def forward(A, b, x):
    return np.tanh(A @ x + b)


def jvp(A, b, x, v):
    y = forward(A, b, x)
    return (1 - y ** 2) * (A @ v)


def vjp(A, b, x, u):
    y = forward(A, b, x)
    return A.T @ ((1 - y ** 2) * u)


def full_jacobian(A, b, x):
    y = forward(A, b, x)
    return (1 - y ** 2)[:, None] * A

import numpy as np


def huber(r, delta):
    """Elementwise Huber loss and its derivative: r^2 / 2 for |r| <= delta, linear beyond."""
    a = np.abs(r)
    value = np.where(a <= delta, 0.5 * r * r, delta * (a - 0.5 * delta))
    return value, np.where(a <= delta, r, delta * np.sign(r))


def hoffmann_objective(theta, N, D, L, delta=1e-3):
    """theta = (a, b, e, alpha, beta), with A = exp(a), B = exp(b), E = exp(e). The predicted log
    loss is LSE(a - alpha log N, b - beta log D, e); return the sum over runs of
    huber(predicted - log L, delta) and its gradient with respect to theta."""
    a, b, e, alpha, beta = theta
    lN, lD = np.log(N), np.log(D)
    z = np.stack([a - alpha * lN, b - beta * lD, np.full(lN.shape, e)])
    m = z.max(axis=0)
    w = np.exp(z - m)
    s = w.sum(axis=0)
    p = w / s
    h, dh = huber(m + np.log(s) - np.log(L), delta)
    grad = np.array([
        np.sum(dh * p[0]),
        np.sum(dh * p[1]),
        np.sum(dh * p[2]),
        -np.sum(dh * p[0] * lN),
        -np.sum(dh * p[1] * lD),
    ])
    return h.sum(), grad

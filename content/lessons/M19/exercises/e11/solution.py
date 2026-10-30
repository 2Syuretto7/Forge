import time

import numpy as np


# provided
def make_net(n, width=32, depth=20, seed=0):
    rng = np.random.default_rng(seed)
    Ws = [rng.normal(size=(width, n)) / np.sqrt(n)] + [rng.normal(size=(width, width)) / np.sqrt(width) for _ in range(depth - 1)]
    return Ws, rng.normal(size=width)


def forward_mode_grad(Ws, w, x):
    """All n JVPs at once through a tangent matrix."""
    h = x
    T = np.eye(x.size)
    for W in Ws:
        h = np.tanh(W @ h)
        T = (1 - h * h)[:, None] * (W @ T)
    return w @ T


def reverse_mode_grad(Ws, w, x):
    """One forward pass, one backward pass of VJPs."""
    hs = [x]
    for W in Ws:
        hs.append(np.tanh(W @ hs[-1]))
    g = w
    for k in range(len(Ws), 0, -1):
        a = g * (1 - hs[k] ** 2)
        g = Ws[k - 1].T @ a
    return g


def time_ratio(n, reps=5):
    """Forward-mode time over reverse-mode time."""
    Ws, w = make_net(n)
    x = np.random.default_rng(1).normal(size=n)
    t0 = time.perf_counter()
    for _ in range(reps):
        forward_mode_grad(Ws, w, x)
    t1 = time.perf_counter()
    for _ in range(reps):
        reverse_mode_grad(Ws, w, x)
    t2 = time.perf_counter()
    return (t1 - t0) / (t2 - t1)

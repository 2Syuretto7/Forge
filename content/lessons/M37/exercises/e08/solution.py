import numpy as np


def _grid(T, steps, tmin):
    return np.geomspace(T, tmin, steps + 1)


def flow_backward(score, x, T, steps, tmin=1e-3):
    """Probability-flow ODE from T down to tmin."""
    ts = _grid(T, steps, tmin)
    x = np.array(x, dtype=float)
    for i in range(steps):
        h = ts[i] - ts[i + 1]
        x = x + h * (x + score(x, ts[i]))
    return x


def flow_forward(score, x, T, steps, tmin=1e-3):
    """Probability-flow ODE from tmin up to T, undoing flow_backward."""
    ts = _grid(T, steps, tmin)
    x = np.array(x, dtype=float)
    for i in reversed(range(steps)):
        h = ts[i] - ts[i + 1]
        x = x - h * (x + score(x, ts[i]))
    return x


def w1(x, y):
    """One-dimensional Wasserstein distance between equal-sized samples."""
    return float(np.mean(np.abs(np.sort(x) - np.sort(y))))

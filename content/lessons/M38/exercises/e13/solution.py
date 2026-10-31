import numpy as np


def steps_to_tol(run, tol=1e-3, max_steps=50000):
    """First step at which every coordinate is below tol."""
    traj = run(max_steps)
    ok = np.all(np.abs(traj) < tol, axis=1)
    idx = np.argmax(ok)
    return int(idx) if ok[idx] else None


def _adam(s, x0, steps, lr=0.01, decay=0.999, b1=0.9, b2=0.999, eps=1e-12):
    x = np.array(x0, dtype=float)
    m, v = np.zeros_like(x), np.zeros_like(x)
    out = [x.copy()]
    for t in range(1, steps + 1):
        g = s * x
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        x = x - lr * decay**t * (m / (1 - b1**t)) / (np.sqrt(v / (1 - b2**t)) + eps)
        out.append(x.copy())
    return np.array(out)


def _gd(s, x0, steps, lr):
    x = np.array(x0, dtype=float)
    out = [x.copy()]
    for _ in range(steps):
        x = x - lr * s * x
        out.append(x.copy())
    return np.array(out)


def compare(scales, x0):
    """Steps to tolerance for gradient descent and Adam."""
    s = np.asarray(scales, dtype=float)
    lr = 1.8 / s.max()
    return {"gd": steps_to_tol(lambda n: _gd(s, x0, n, lr)), "adam": steps_to_tol(lambda n: _adam(s, x0, n))}

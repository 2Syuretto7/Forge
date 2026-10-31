import numpy as np


def run_adam(grad, x0, steps, lr, b1=0.9, b2=0.999, eps=1e-12):
    """Adam trajectory."""
    x = np.array(x0, dtype=float)
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    out = [x.copy()]
    for t in range(1, steps + 1):
        g = grad(x)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        x = x - lr * (m / (1 - b1**t)) / (np.sqrt(v / (1 - b2**t)) + eps)
        out.append(x.copy())
    return np.array(out)


def run_sgd(grad, x0, steps, lr):
    """Gradient descent trajectory."""
    x = np.array(x0, dtype=float)
    out = [x.copy()]
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(steps):
            x = x - lr * grad(x)
            out.append(x.copy())
    return np.array(out)


def quadratic_grad(scales):
    """Gradient of sum_i s_i x_i^2 / 2."""
    s = np.asarray(scales, dtype=float)
    return lambda x: s * x

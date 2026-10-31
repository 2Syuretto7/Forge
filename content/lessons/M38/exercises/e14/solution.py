import numpy as np


def uncorrected_step_sizes(g, steps, lr=1.0, b1=0.9, b2=0.999):
    """Update sizes without bias correction for a constant gradient."""
    m = v = 0.0
    out = []
    for _ in range(steps):
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        out.append(lr * abs(m) / np.sqrt(v))
    return np.array(out)


def corrected_step_sizes(g, steps, lr=1.0, b1=0.9, b2=0.999):
    """Update sizes with bias correction for a constant gradient."""
    m = v = 0.0
    out = []
    for t in range(1, steps + 1):
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        out.append(lr * abs(m / (1 - b1**t)) / np.sqrt(v / (1 - b2**t)))
    return np.array(out)


def peak_ratio(b1, b2, steps=2000):
    """Largest uncorrected step over the corrected one."""
    return float(np.max(uncorrected_step_sizes(1.0, steps, 1.0, b1, b2)))

import math


def online_grad(t, C=3.0):
    """Gradient of the t-th online loss."""
    return C if t % 3 == 1 else -1.0


def run(amsgrad, steps=30000, C=3.0):
    """Projected Adam or AMSGrad on the online problem."""
    b2 = 1 / (1 + C * C)
    x, v, vmax = 0.0, 0.0, 0.0
    for t in range(1, steps + 1):
        g = online_grad(t, C)
        v = b2 * v + (1 - b2) * g * g
        vmax = max(vmax, v)
        x -= 0.5 / math.sqrt(t) * g / (math.sqrt(vmax if amsgrad else v) + 1e-12)
        x = min(1.0, max(-1.0, x))
    return x


def average_loss_slope(C=3.0):
    """Slope of the average loss."""
    return (C - 2) / 3

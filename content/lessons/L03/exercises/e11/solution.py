import numpy as np


def taylor2(f0, g, H, h):
    return float(f0 + g @ h + 0.5 * h @ H @ h)


def descent_bound(gnorm2, L, eta):
    return eta * gnorm2 - 0.5 * L * eta ** 2 * gnorm2


def gd_step_decrease(f, grad, x, eta):
    return float(f(x) - f(x - eta * grad(x)))

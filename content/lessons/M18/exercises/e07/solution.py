def taylor2(f0, g, H, h):
    """Second-order Taylor prediction."""
    return float(f0 + g @ h + 0.5 * h @ H @ h)


def descent_bound(gnorm2, L, eta):
    """Guaranteed decrease of one gradient step."""
    return eta * gnorm2 - 0.5 * L * eta ** 2 * gnorm2


def gd_step_decrease(f, grad, x, eta):
    """Actual decrease of one gradient step."""
    return float(f(x) - f(x - eta * grad(x)))

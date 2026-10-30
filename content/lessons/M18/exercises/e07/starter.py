def taylor2(f0, g, H, h):
    """Second-order Taylor prediction."""
    raise NotImplementedError


def descent_bound(gnorm2, L, eta):
    """Guaranteed decrease of one gradient step."""
    raise NotImplementedError


def gd_step_decrease(f, grad, x, eta):
    """Actual decrease of one gradient step."""
    raise NotImplementedError

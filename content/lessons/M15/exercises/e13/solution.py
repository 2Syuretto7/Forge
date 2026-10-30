def estimates_at_zero(f, h):
    """Forward, backward and central differences at 0."""
    fwd = (f(h) - f(0.0)) / h
    bwd = (f(0.0) - f(-h)) / h
    return {"forward": fwd, "backward": bwd, "central": (f(h) - f(-h)) / (2 * h)}


def looks_differentiable(f, a, hs=(1e-2, 1e-4, 1e-6)):
    """Whether forward and backward differences agree at each step."""
    for h in hs:
        fwd = (f(a + h) - f(a)) / h
        bwd = (f(a) - f(a - h)) / h
        if abs(fwd - bwd) > 1e-3:
            return False
    return True

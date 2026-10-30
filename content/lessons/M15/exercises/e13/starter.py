def estimates_at_zero(f, h):
    """Forward, backward and central differences at 0."""
    raise NotImplementedError


def looks_differentiable(f, a, hs=(1e-2, 1e-4, 1e-6)):
    """Whether forward and backward differences agree at each step."""
    raise NotImplementedError

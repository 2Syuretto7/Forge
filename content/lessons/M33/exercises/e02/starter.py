def attainable(I, peak, bw):
    """Roofline: attainable flops per second."""
    raise NotImplementedError


def ridge_point(peak, bw):
    """Intensity where memory and compute limits meet."""
    raise NotImplementedError


def bound(I, peak, bw):
    """Which roof limits a kernel."""
    raise NotImplementedError


def time_estimate(flops, nbytes, peak, bw):
    """Lower bound on running time."""
    raise NotImplementedError

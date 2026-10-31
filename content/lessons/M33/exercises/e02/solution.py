def attainable(I, peak, bw):
    """Roofline: attainable flops per second."""
    return min(peak, I * bw)


def ridge_point(peak, bw):
    """Intensity where memory and compute limits meet."""
    return peak / bw


def bound(I, peak, bw):
    """Which roof limits a kernel."""
    return "memory" if I < peak / bw else "compute"


def time_estimate(flops, nbytes, peak, bw):
    """Lower bound on running time."""
    return max(flops / peak, nbytes / bw)

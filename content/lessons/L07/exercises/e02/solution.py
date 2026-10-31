T4 = {"fp32": 8.1e12, "fp16": 65e12, "bw": 320e9}


def ridge(peak, bw):
    """Arithmetic intensity (FLOP/byte) where the memory and compute roofs meet."""
    return peak / bw


def roofline_time(flops, nbytes, peak, bw):
    """Lower bound on the runtime: the slower of computing and moving the data."""
    return max(flops / peak, nbytes / bw)


def bound(flops, nbytes, peak, bw):
    """"memory" or "compute", whichever roof limits this kernel."""
    return "memory" if flops / nbytes < ridge(peak, bw) else "compute"


def efficiency(flops, nbytes, measured_seconds, peak, bw):
    """Fraction of the roofline bound achieved by a measured run."""
    return roofline_time(flops, nbytes, peak, bw) / measured_seconds

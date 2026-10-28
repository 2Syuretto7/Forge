T4 = {"fp32": 8.1e12, "fp16": 65e12, "bw": 320e9}


def ridge(peak, bw):
    """Arithmetic intensity (FLOP/byte) where the memory and compute roofs meet."""
    raise NotImplementedError


def roofline_time(flops, nbytes, peak, bw):
    """Lower bound on the runtime: the slower of computing and moving the data."""
    raise NotImplementedError


def bound(flops, nbytes, peak, bw):
    """"memory" or "compute", whichever roof limits this kernel."""
    raise NotImplementedError


def efficiency(flops, nbytes, measured_seconds, peak, bw):
    """Fraction of the roofline bound achieved by a measured run."""
    raise NotImplementedError

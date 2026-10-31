def kernel_time(flops, nbytes, peak, bw):
    return max(flops / peak, nbytes / bw)


def step_time(kernels, peak, bw, launch_s=10e-6):
    """Kernels run one after another. The CPU needs launch_s to issue each one, and the GPU cannot
    start a kernel before it is issued, so each costs the larger of its GPU time and launch_s."""
    raise NotImplementedError


def launch_bound_fraction(kernels, peak, bw, launch_s=10e-6):
    """Fraction of kernels whose GPU time is shorter than the launch overhead."""
    raise NotImplementedError

def collective_time(op, n_bytes, P, alpha, bandwidth):
    """Ring collectives under the alpha-beta model: every step costs a latency alpha, and each rank
    sends (P - 1) / P of the data per pass at `bandwidth` bytes per second. reduce_scatter and
    all_gather take P - 1 steps and one pass; all_reduce is both: 2 (P - 1) steps and two passes.
    One rank (P = 1) costs nothing."""
    raise NotImplementedError


def dp_step_time(n_params, P, alpha, bandwidth, compute_seconds, overlap):
    """One data-parallel step: the compute, plus the all-reduce of 2-byte gradients. With
    overlap, communication hides behind compute and the step takes the longer of the two."""
    raise NotImplementedError

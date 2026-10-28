def collective_time(op, n_bytes, P, alpha, bandwidth):
    """Ring collectives under the alpha-beta model: every step costs a latency alpha, and each rank
    sends (P - 1) / P of the data per pass at `bandwidth` bytes per second. reduce_scatter and
    all_gather take P - 1 steps and one pass; all_reduce is both: 2 (P - 1) steps and two passes.
    One rank (P = 1) costs nothing."""
    if P == 1:
        return 0.0
    passes = {"reduce_scatter": 1, "all_gather": 1, "all_reduce": 2}[op]
    return passes * ((P - 1) * alpha + (P - 1) / P * n_bytes / bandwidth)


def dp_step_time(n_params, P, alpha, bandwidth, compute_seconds, overlap):
    """One data-parallel step: the compute, plus the all-reduce of 2-byte gradients. With
    overlap, communication hides behind compute and the step takes the longer of the two."""
    comm = collective_time("all_reduce", 2 * n_params, P, alpha, bandwidth)
    return max(compute_seconds, comm) if overlap else compute_seconds + comm

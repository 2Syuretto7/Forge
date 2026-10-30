def solve_linear(a, b, c):
    """Solve a x + b = c: a float, "all" for every x, or None for no solution."""
    if a == 0:
        return "all" if b == c else None
    return (c - b) / a


def utilization(hours, n_params, n_tokens, peak_flops):
    """The utilization u at which 6 N D FLOPs take `hours` GPU-hours at the given peak."""
    return 6 * n_params * n_tokens / (peak_flops * 3600 * hours)

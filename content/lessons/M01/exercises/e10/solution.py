def tokens_for(n_params, tokens_per_param=20):
    """Training tokens at a fixed number of tokens per parameter."""
    return n_params * tokens_per_param


def gpu_hours(n_params, n_tokens, flops_per_s, utilization=0.4):
    """GPU-hours for 6 N D FLOPs at a sustained rate flops_per_s * utilization."""
    seconds = 6 * n_params * n_tokens / (flops_per_s * utilization)
    return seconds / 3600


def wall_clock_days(n_gpu_hours, n_gpus):
    """Days of wall-clock time for the run on n_gpus GPUs."""
    return n_gpu_hours / n_gpus / 24


def run_cost(n_gpu_hours, price_per_hour):
    """Cost in dollars."""
    return n_gpu_hours * price_per_hour

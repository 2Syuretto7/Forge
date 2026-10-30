def tokens_for(n_params, tokens_per_param=20):
    """Training tokens at a fixed number of tokens per parameter."""
    raise NotImplementedError


def gpu_hours(n_params, n_tokens, flops_per_s, utilization=0.4):
    """GPU-hours for 6 N D FLOPs at a sustained rate flops_per_s * utilization."""
    raise NotImplementedError


def wall_clock_days(n_gpu_hours, n_gpus):
    """Days of wall-clock time for the run on n_gpus GPUs."""
    raise NotImplementedError


def run_cost(n_gpu_hours, price_per_hour):
    """Cost in dollars."""
    raise NotImplementedError

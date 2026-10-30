import math

SLIPS = {
    "seconds vs hours": 3600,
    "minutes vs hours": 60,
    "hours vs days": 24,
    "seconds vs days": 86400,
    "bits vs bytes": 8,
    "kilo vs unit": 1000,
    "GB vs GiB": 2 ** 30 / 10 ** 9,
    "KB vs KiB": 1024 / 1000,
    "16-bit vs 32-bit numbers": 2,
}


# provided
def colleague_gpu_hours(n_params, n_tokens, flops_per_s):
    """The colleague's estimate. Provided: do not change it."""
    flops = 6 * n_params * n_tokens
    return flops / flops_per_s


def gpu_hours(n_params, n_tokens, flops_per_s):
    """Correct GPU-hours at full utilization."""
    return 6 * n_params * n_tokens / flops_per_s / 3600


def error_factor(n_params, n_tokens, flops_per_s):
    """The colleague's answer divided by the correct one."""
    return colleague_gpu_hours(n_params, n_tokens, flops_per_s) / gpu_hours(n_params, n_tokens, flops_per_s)


def diagnose(ratio):
    """Name of the slip in SLIPS closest to ratio on a log scale, or None beyond 2 percent."""
    r = max(ratio, 1 / ratio)
    name, f = min(SLIPS.items(), key=lambda kv: abs(math.log(r / kv[1])))
    return name if max(r / f, f / r) <= 1.02 else None

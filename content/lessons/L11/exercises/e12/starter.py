def pipelined_time(steps, cpu_s, gpu_s):
    """The CPU issues work for step i + 1 while the GPU runs step i: after the first step, each step
    costs the slower of the two."""
    raise NotImplementedError


def synced_time(steps, cpu_s, gpu_s):
    """A .item() (or print of a GPU value) at the end of every step makes the CPU wait for the GPU,
    so nothing overlaps."""
    raise NotImplementedError


def sync_slowdown(steps, cpu_s, gpu_s):
    raise NotImplementedError

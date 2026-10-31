def summarize(events):
    """events: dicts with "name", "start" and "dur" (microseconds) for kernels on one GPU stream.
    Return {name: (count, total_us)} sorted by total time, largest first."""
    raise NotImplementedError


def gpu_idle_fraction(events):
    """Fraction of the span from the first kernel's start to the last kernel's end with no kernel
    running (kernels on one stream do not overlap)."""
    raise NotImplementedError


def top_fraction(events, k=1):
    """Share of all kernel time taken by the k most expensive kernel names."""
    raise NotImplementedError

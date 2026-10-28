def transfer_time(nbytes, bw, latency_s=10e-6):
    """Time to copy nbytes across PCIe at bandwidth bw (bytes/s) with a fixed per-copy latency."""
    return latency_s + nbytes / bw


def effective_bandwidth(nbytes, bw, latency_s=10e-6):
    return nbytes / transfer_time(nbytes, bw, latency_s)


def input_pipeline_time(batch_bytes, compute_s, bw, overlap):
    """Per-step time when every batch is copied to the GPU first. Without overlap, copy then compute;
    with overlap (pinned memory, non_blocking copies of the next batch), the slower of the two."""
    t = transfer_time(batch_bytes, bw)
    return max(t, compute_s) if overlap else t + compute_s

def throughput(batch, weight_bytes, kv_bytes_per_seq, bandwidth):
    """Tokens per second of memory-bound decoding: each step reads the weights and every
    sequence's cache once and produces one token per sequence."""
    return batch * bandwidth / (weight_bytes + batch * kv_bytes_per_seq)


def marginal_throughput(batch, weight_bytes, kv_bytes_per_seq, bandwidth):
    """The derivative of throughput with respect to the batch size."""
    return bandwidth * weight_bytes / (weight_bytes + batch * kv_bytes_per_seq) ** 2


def largest_batch_within(latency_s, weight_bytes, kv_bytes_per_seq, bandwidth, limit=4096):
    """The largest batch (up to limit) whose decode step stays within latency_s; 0 if none."""
    best = 0
    for b in range(1, limit + 1):
        if (weight_bytes + b * kv_bytes_per_seq) / bandwidth <= latency_s:
            best = b
    return best

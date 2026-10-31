def throughput(batch, weight_bytes, kv_bytes_per_seq, bandwidth):
    """Tokens per second of memory-bound decoding: each step reads the weights and every
    sequence's cache once and produces one token per sequence."""
    raise NotImplementedError


def marginal_throughput(batch, weight_bytes, kv_bytes_per_seq, bandwidth):
    """The derivative of throughput with respect to the batch size."""
    raise NotImplementedError


def largest_batch_within(latency_s, weight_bytes, kv_bytes_per_seq, bandwidth, limit=4096):
    """The largest batch (up to limit) whose decode step stays within latency_s; 0 if none."""
    raise NotImplementedError

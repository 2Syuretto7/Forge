def index_bytes(n, d, bytes_per=4):
    """Memory for n vectors of length d."""
    return n * d * bytes_per


def query_seconds(n, d, flops_per_s):
    """Seconds per brute-force query."""
    return 2 * n * d / flops_per_s


def max_vectors(memory_bytes, d, bytes_per=4):
    """Vectors that fit in memory."""
    return memory_bytes // (d * bytes_per)


def queries_per_second(n, d, flops_per_s):
    """1 / query_seconds."""
    return 1 / query_seconds(n, d, flops_per_s)

def index_bytes(n, d, bytes_per=4):
    """Memory for n vectors of length d."""
    raise NotImplementedError


def query_seconds(n, d, flops_per_s):
    """Seconds per brute-force query."""
    raise NotImplementedError


def max_vectors(memory_bytes, d, bytes_per=4):
    """Vectors that fit in memory."""
    raise NotImplementedError


def queries_per_second(n, d, flops_per_s):
    """1 / query_seconds."""
    raise NotImplementedError

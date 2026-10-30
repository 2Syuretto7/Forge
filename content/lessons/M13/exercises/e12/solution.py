def dense_bytes(n):
    """Bytes of a dense float64 n x n matrix."""
    return 8 * n * n


def sparse_bytes(nnz, index_bytes=4, value_bytes=8):
    """Bytes of an edge list with weights."""
    return nnz * (2 * index_bytes + value_bytes)


def iteration_flops(nnz, n):
    """Operations in one sparse step."""
    return 2 * nnz + 3 * n


def seconds(n, nnz, steps, flops_per_s):
    """Total time of steps iterations."""
    return steps * iteration_flops(nnz, n) / flops_per_s

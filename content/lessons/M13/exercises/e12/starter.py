def dense_bytes(n):
    """Bytes of a dense float64 n x n matrix."""
    raise NotImplementedError


def sparse_bytes(nnz, index_bytes=4, value_bytes=8):
    """Bytes of an edge list with weights."""
    raise NotImplementedError


def iteration_flops(nnz, n):
    """Operations in one sparse step."""
    raise NotImplementedError


def seconds(n, nnz, steps, flops_per_s):
    """Total time of steps iterations."""
    raise NotImplementedError

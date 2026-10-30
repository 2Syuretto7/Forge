def _parts(s1, s2):
    raise NotImplementedError


def matmul_shape(s1, s2):
    """Shape of A @ B."""
    raise NotImplementedError


def matmul_flops(s1, s2):
    """2 m n p per product, times the batch size."""
    raise NotImplementedError

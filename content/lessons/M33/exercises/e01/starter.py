def matmul_flops(m, n, k):
    """Floating-point operations of an (m x k) by (k x n) product."""
    raise NotImplementedError


def matmul_bytes(m, n, k, word=4):
    """Minimal bytes moved: read A and B once, write C once."""
    raise NotImplementedError


def intensity(flops, nbytes):
    """Flops per byte."""
    raise NotImplementedError


def matvec_intensity(m, n, word=4):
    """Arithmetic intensity of a matrix-vector product."""
    raise NotImplementedError

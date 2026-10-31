def matmul_flops(m, n, k):
    """Floating-point operations of an (m x k) by (k x n) product."""
    return 2 * m * n * k


def matmul_bytes(m, n, k, word=4):
    """Minimal bytes moved: read A and B once, write C once."""
    return (m * k + k * n + m * n) * word


def intensity(flops, nbytes):
    """Flops per byte."""
    return flops / nbytes


def matvec_intensity(m, n, word=4):
    """Arithmetic intensity of a matrix-vector product."""
    return 2 * m * n / ((m * n + n + m) * word)

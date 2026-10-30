def scores_bytes(batch, heads, T, bytes_per=2):
    """Bytes of the (batch, heads, T, T) score tensor."""
    return batch * heads * T * T * bytes_per


def matmul_bytes(m, n, p, bytes_per=2):
    """Bytes moved by one product if each matrix moves once."""
    return (m * n + n * p + m * p) * bytes_per


def intensity(m, n, p, bytes_per=2):
    """Operations per byte."""
    return 2 * m * n * p / matmul_bytes(m, n, p, bytes_per)

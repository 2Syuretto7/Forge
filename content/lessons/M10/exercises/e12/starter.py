def scores_bytes(batch, heads, T, bytes_per=2):
    """Bytes of the (batch, heads, T, T) score tensor."""
    raise NotImplementedError


def matmul_bytes(m, n, p, bytes_per=2):
    """Bytes moved by one product if each matrix moves once."""
    raise NotImplementedError


def intensity(m, n, p, bytes_per=2):
    """Operations per byte."""
    raise NotImplementedError

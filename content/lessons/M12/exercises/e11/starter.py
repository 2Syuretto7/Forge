def flops_normal(m, n):
    """A^T A (symmetric), A^T b, Cholesky."""
    raise NotImplementedError


def flops_qr(m, n):
    """Householder QR, Q^T b, back substitution."""
    raise NotImplementedError


def ratio(m, n):
    """QR cost over normal-equations cost."""
    raise NotImplementedError

def flops_normal(m, n):
    """A^T A (symmetric), A^T b, Cholesky."""
    return m * n * n + 2 * m * n + n ** 3 / 3


def flops_qr(m, n):
    """Householder QR, Q^T b, back substitution."""
    return 2 * m * n * n - 2 * n ** 3 / 3 + 4 * m * n + n * n


def ratio(m, n):
    """QR cost over normal-equations cost."""
    return flops_qr(m, n) / flops_normal(m, n)

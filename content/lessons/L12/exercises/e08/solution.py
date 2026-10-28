def standard_io(N, d):
    """Elements moved by unfused attention: read Q, K, V and write O (4Nd), plus write and read the
    N x N scores and probabilities (4N^2)."""
    return 4 * N * d + 4 * N * N


def flash_io(N, d, M):
    """Elements moved by FlashAttention with on-chip memory of M elements: blocks of about M / (4d) keys
    and values, and the Q, O blocks re-read once per key block: about N^2 d^2 / M plus 4Nd."""
    return N * N * d * d / M + 4 * N * d


def io_ratio(N, d, M):
    return standard_io(N, d) / flash_io(N, d, M)

def storage(m, n, k):
    """Numbers in a rank-k factorization."""
    return k * (m + n + 1)


def matvec_cost(m, n, k=None):
    """Operations for A x, full or through rank-k factors."""
    return 2 * m * n if k is None else 2 * k * (m + n) + k


def break_even_rank(m, n):
    """Largest k with storage below m n."""
    return (m * n - 1) // (m + n + 1)


def gram_flops(m, n):
    """Forming X^T X with symmetry."""
    return m * n * n

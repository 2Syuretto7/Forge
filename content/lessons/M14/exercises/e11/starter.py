def storage(m, n, k):
    """Numbers in a rank-k factorization."""
    raise NotImplementedError


def matvec_cost(m, n, k=None):
    """Operations for A x, full or through rank-k factors."""
    raise NotImplementedError


def break_even_rank(m, n):
    """Largest k with storage below m n."""
    raise NotImplementedError


def gram_flops(m, n):
    """Forming X^T X with symmetry."""
    raise NotImplementedError

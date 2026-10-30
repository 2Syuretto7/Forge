import numpy as np


def block_matmul(A, B, bs):
    """AB computed tile by tile."""
    m, n = A.shape
    p = B.shape[1]
    C = np.zeros((m, p))
    for i in range(0, m, bs):
        for j in range(0, p, bs):
            for k in range(0, n, bs):
                C[i:i + bs, j:j + bs] += A[i:i + bs, k:k + bs] @ B[k:k + bs, j:j + bs]
    return C


def tile_count(m, n, p, bs):
    """Number of tile products."""
    return (-(-m // bs)) * (-(-n // bs)) * (-(-p // bs))

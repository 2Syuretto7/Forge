import math
import numpy as np


def blocked_matmul(A, B, b):
    """Tile-by-tile matrix product."""
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    m, k = A.shape
    n = B.shape[1]
    C = np.zeros((m, n))
    for i0 in range(0, m, b):
        for j0 in range(0, n, b):
            for p0 in range(0, k, b):
                C[i0 : i0 + b, j0 : j0 + b] += A[i0 : i0 + b, p0 : p0 + b] @ B[p0 : p0 + b, j0 : j0 + b]
    return C


def traffic_naive(n):
    """Words moved by the naive triple loop."""
    return 2 * n**3 + n**2


def traffic_blocked(n, b):
    """Words moved by the blocked algorithm with b x b tiles."""
    return 2 * n**3 / b + n**2


def best_tile(cache_words):
    """Largest tile with three tiles in cache."""
    b = math.isqrt(cache_words // 3)
    while 3 * (b + 1) ** 2 <= cache_words:
        b += 1
    while 3 * b * b > cache_words:
        b -= 1
    return b

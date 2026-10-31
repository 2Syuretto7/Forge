import numpy as np


def tiled_matmul(A, B, T):
    """C = A B computed in T x T output tiles, looping over K in steps of T, with sizes that need not be
    multiples of T. Return (C, loads), where loads counts the elements read from A and B."""
    M, K = A.shape
    N = B.shape[1]
    C = np.zeros((M, N))
    loads = 0
    for i in range(0, M, T):
        for j in range(0, N, T):
            acc = np.zeros((min(T, M - i), min(T, N - j)))
            for k in range(0, K, T):
                a = A[i:i + T, k:k + T]
                b = B[k:k + T, j:j + T]
                loads += a.size + b.size
                acc += a @ b
            C[i:i + T, j:j + T] = acc
    return C, loads

def matmul(A, B):
    """Naive product of square list-of-rows matrices; (C, multiply_adds)."""
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    count = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                count += 1
    return C, count


def predicted_multiply_adds(n):
    """n^3."""
    return n ** 3


def predicted_ratio(n):
    """Cost at 2n over cost at n."""
    return predicted_multiply_adds(2 * n) / predicted_multiply_adds(n)

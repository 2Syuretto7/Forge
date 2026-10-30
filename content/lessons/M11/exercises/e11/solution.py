def lu_flops(n):
    """Operations in LU of an n by n matrix."""
    return sum(j + 2 * j * j for j in range(1, n))


def tri_flops(n):
    """Operations in one triangular solve."""
    return n * n


def many_rhs_flops(n, k, refactor):
    """Operations for k right-hand sides."""
    per_solve = 2 * tri_flops(n)
    if refactor:
        return k * (lu_flops(n) + per_solve)
    return lu_flops(n) + k * per_solve

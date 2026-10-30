def lu_flops(n):
    """Operations in LU of an n by n matrix."""
    raise NotImplementedError


def tri_flops(n):
    """Operations in one triangular solve."""
    raise NotImplementedError


def many_rhs_flops(n, k, refactor):
    """Operations for k right-hand sides."""
    raise NotImplementedError

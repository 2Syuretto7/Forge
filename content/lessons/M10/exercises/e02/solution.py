import numpy as np


def _check(A, B):
    if A.shape[1] != B.shape[0]:
        raise ValueError(f"inner sizes differ: {A.shape} and {B.shape}")


def by_dots(A, B):
    """Entry (i, j) = row i of A . column j of B."""
    _check(A, B)
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            C[i, j] = np.sum(A[i, :] * B[:, j])
    return C


def by_columns(A, B):
    """Column j = combination of the columns of A with weights B[:, j]."""
    _check(A, B)
    C = np.zeros((A.shape[0], B.shape[1]))
    for j in range(B.shape[1]):
        C[:, j] = sum(B[k, j] * A[:, k] for k in range(A.shape[1]))
    return C


def by_outer(A, B):
    """Sum of outer products of the columns of A with the rows of B."""
    _check(A, B)
    C = np.zeros((A.shape[0], B.shape[1]))
    for k in range(A.shape[1]):
        C += np.outer(A[:, k], B[k, :])
    return C

import numpy as np


def _check(A, B):
    raise NotImplementedError


def by_dots(A, B):
    """Entry (i, j) = row i of A . column j of B."""
    raise NotImplementedError


def by_columns(A, B):
    """Column j = combination of the columns of A with weights B[:, j]."""
    raise NotImplementedError


def by_outer(A, B):
    """Sum of outer products of the columns of A with the rows of B."""
    raise NotImplementedError

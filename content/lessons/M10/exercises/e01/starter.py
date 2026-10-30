def _check(A, x):
    raise NotImplementedError


def matvec_rows(A, x):
    """Each output is a row of A dotted with x."""
    raise NotImplementedError


def matvec_cols(A, x):
    """The combination of the columns of A with weights x."""
    raise NotImplementedError

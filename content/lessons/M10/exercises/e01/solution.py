def _check(A, x):
    if any(len(row) != len(x) for row in A):
        raise ValueError("shapes do not fit")


def matvec_rows(A, x):
    """Each output is a row of A dotted with x."""
    _check(A, x)
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def matvec_cols(A, x):
    """The combination of the columns of A with weights x."""
    _check(A, x)
    out = [0.0] * len(A)
    for j, w in enumerate(x):
        for i, row in enumerate(A):
            out[i] += w * row[j]
    return out

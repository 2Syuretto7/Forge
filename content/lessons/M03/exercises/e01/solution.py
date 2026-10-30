import itertools


def implies(p, q):
    """Truth value of p implies q."""
    return (not p) or q


def truth_table(f, n):
    """All 2**n rows (inputs, f(*inputs)), True before False, first input slowest."""
    return [(row, f(*row)) for row in itertools.product([True, False], repeat=n)]


def count_true(f, n):
    """Number of rows where f is true."""
    return sum(1 for _, v in truth_table(f, n) if v)

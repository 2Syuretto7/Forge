import itertools


def implies(p, q):
    """Truth value of p implies q."""
    raise NotImplementedError


def truth_table(f, n):
    """All 2**n rows (inputs, f(*inputs)), True before False, first input slowest."""
    raise NotImplementedError


def count_true(f, n):
    """Number of rows where f is true."""
    raise NotImplementedError

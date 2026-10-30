def union(A, B):
    """Elements in A or B, without repeats."""
    out = list(A)
    for b in B:
        if b not in out:
            out.append(b)
    return out


def intersection(A, B):
    """Elements in both A and B."""
    return [a for a in A if a in B]


def difference(A, B):
    """Elements of A not in B."""
    return [a for a in A if a not in B]


def is_subset(A, B):
    """Every element of A is in B."""
    return all(a in B for a in A)


def product(A, B):
    """All pairs (a, b)."""
    return [(a, b) for a in A for b in B]


def power_set(A):
    """All subsets of A, each a list."""
    if not A:
        return [[]]
    rest = power_set(A[1:])
    return rest + [[A[0]] + s for s in rest]

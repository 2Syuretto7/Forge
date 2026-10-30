import math

BLOCK = 8


# provided
def sum_list(n):
    ops = 0
    total = 0
    for i in range(n):
        if i > 0:
            ops += 1
        total += i
    return {"ops": ops}


# provided
def all_pairs(n):
    ops = 0
    for i in range(n):
        for j in range(i + 1, n):
            ops += 1
    return {"ops": ops}


# provided
def all_triples(n):
    ops = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                ops += 1
    return {"ops": ops}


# provided
def prefix_naive(n):
    ops = 0
    for i in range(1, n + 1):
        ops += i - 1  # adding i numbers takes i - 1 additions
    return {"ops": ops}


# provided
def prefix_running(n):
    return {"ops": max(0, n - 1)}


# provided
def binary_search(n):
    lo, hi, ops = 0, n, 0
    while lo < hi:
        mid = (lo + hi) // 2
        ops += 1
        lo = mid + 1  # the target is larger than every element: the worst case
    return {"ops": ops}


# provided
def matmul_naive(n):
    ops = loads = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ops += 1
                loads += 2  # A[i][k] and B[k][j] come from slow memory every time
    return {"ops": ops, "loads": loads}


# provided
def matmul_blocked(n):
    b = BLOCK
    ops = loads = 0
    for bi in range(0, n, b):
        for bj in range(0, n, b):
            for bk in range(0, n, b):
                loads += 2 * b * b  # one block of A and one of B, loaded once
                ops += b * b * b
    return {"ops": ops, "loads": loads}


ALGORITHMS = {
    "sum_list": sum_list,
    "all_pairs": all_pairs,
    "all_triples": all_triples,
    "prefix_naive": prefix_naive,
    "prefix_running": prefix_running,
    "binary_search": binary_search,
    "matmul_naive": matmul_naive,
    "matmul_blocked": matmul_blocked,
}

# your answer
FORMULAS = {
    "sum_list": None,
    "all_pairs": None,
    "all_triples": None,
    "prefix_naive": None,
    "prefix_running": None,
    "binary_search": None,
    "matmul_naive": None,
    "matmul_blocked": None,
}

# your answer
LOAD_FORMULAS = {
    "matmul_naive": None,
    "matmul_blocked": None,
}

# your answer
STEPS = {
    "sum_list": None,
    "all_pairs": None,
    "all_triples": None,
    "prefix_naive": None,
    "prefix_running": None,
    "binary_search": None,
    "matmul_naive": None,
    "matmul_blocked": None,
}


def predicted_ratio(name, n):
    """FORMULAS[name](2n) / FORMULAS[name](n)."""
    raise NotImplementedError

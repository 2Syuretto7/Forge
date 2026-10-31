def matmul_cost(m, n, k, bytes_per=2):
    """C = A B with A (m, k) and B (k, n): FLOPs and the minimum bytes moved (read A and B, write C)."""
    raise NotImplementedError


def elementwise_cost(n_elems, flops_per_elem, n_inputs, bytes_per=2):
    """An elementwise op reading n_inputs arrays and writing one."""
    raise NotImplementedError


def softmax_cost(rows, cols, bytes_per=2):
    """Row softmax counted as 5 FLOPs per element (max, subtract, exp, sum, divide); read once, write once."""
    raise NotImplementedError


def intensity(cost):
    flops, nbytes = cost
    return flops / nbytes

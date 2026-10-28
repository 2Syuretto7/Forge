import numpy as np


def ulp(x, exp_bits=5, man_bits=10):
    """Spacing between representable numbers at |x| (subnormal spacing below the normal range)."""
    bias = 2 ** (exp_bits - 1) - 1
    a = abs(x)
    e = max(np.floor(np.log2(a)) if a > 0 else 1 - bias, 1 - bias)
    return 2.0 ** (e - man_bits)


def largest_exact_integer(man_bits):
    """Every integer up to 2^(man_bits + 1) is exactly representable; the next one is not."""
    return 2 ** (man_bits + 1)

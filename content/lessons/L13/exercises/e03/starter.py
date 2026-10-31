import numpy as np


def ulp(x, exp_bits=5, man_bits=10):
    """Spacing between representable numbers at |x| (subnormal spacing below the normal range)."""
    raise NotImplementedError


def largest_exact_integer(man_bits):
    """Every integer up to 2^(man_bits + 1) is exactly representable; the next one is not."""
    raise NotImplementedError

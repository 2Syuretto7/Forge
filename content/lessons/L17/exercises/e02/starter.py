import numpy as np


def format_properties(exp_bits, man_bits):
    """Largest finite value, smallest normal, smallest subnormal and machine epsilon (the gap
    between 1 and the next representable number)."""
    raise NotImplementedError


def decimal_digits(man_bits):
    """Roughly how many significant decimal digits the format keeps: (man_bits + 1) log10 2."""
    raise NotImplementedError

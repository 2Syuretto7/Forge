import numpy as np


def format_properties(exp_bits, man_bits):
    """Largest finite value, smallest normal, smallest subnormal and machine epsilon (the gap
    between 1 and the next representable number)."""
    bias = 2 ** (exp_bits - 1) - 1
    emax = 2 ** exp_bits - 2 - bias
    return {
        "max": (2 - 2.0 ** -man_bits) * 2.0 ** emax,
        "min_normal": 2.0 ** (1 - bias),
        "min_subnormal": 2.0 ** (1 - bias - man_bits),
        "eps": 2.0 ** -man_bits,
    }


def decimal_digits(man_bits):
    """Roughly how many significant decimal digits the format keeps: (man_bits + 1) log10 2."""
    return (man_bits + 1) * np.log10(2)

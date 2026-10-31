import numpy as np


def round_to_format(x, exp_bits, man_bits):
    """Round float64 values to the nearest value representable with exp_bits exponent bits and
    man_bits mantissa bits (IEEE layout: bias 2^(e-1) - 1, subnormals, infinities), ties to even.
    Values beyond the largest finite number become +-inf."""
    raise NotImplementedError

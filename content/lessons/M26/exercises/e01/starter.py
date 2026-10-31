import math
import struct
import numpy as np


def float32_bits(x):
    """The 32-bit pattern of x rounded to float32."""
    raise NotImplementedError


def decode(bits):
    """(sign, exponent, fraction, value) of a float32 bit pattern."""
    raise NotImplementedError


def spacing(x):
    """Gap to the next larger float32."""
    raise NotImplementedError

import numpy as np


def round_to_format(x, exp_bits, man_bits):
    """Round float64 values to the nearest value representable with exp_bits exponent bits and
    man_bits mantissa bits (IEEE layout: bias 2^(e-1) - 1, subnormals, infinities), ties to even.
    Values beyond the largest finite number become +-inf."""
    x = np.asarray(x, dtype=np.float64)
    bias = 2 ** (exp_bits - 1) - 1
    emin = 1 - bias
    emax = 2 ** exp_bits - 2 - bias
    max_finite = (2 - 2.0 ** -man_bits) * 2.0 ** emax
    a = np.abs(x)
    with np.errstate(divide="ignore"):
        e = np.floor(np.log2(np.where(a > 0, a, 1.0)))
    e = np.maximum(e, emin)
    ulp = 2.0 ** (e - man_bits)
    r = np.round(a / ulp) * ulp  # np.round rounds halves to even
    r = np.where(r > max_finite, np.inf, r)
    return np.sign(x) * r


def bf16(x):
    """Round float values to bfloat16 (8 exponent bits, 7 mantissa bits)."""
    return round_to_format(x, 8, 7)


def fp16(x):
    return round_to_format(x, 5, 10)


def survives(x, fmt):
    """True where the value is finite and nonzero after rounding (it neither overflowed nor
    underflowed)."""
    r = fmt(x)
    return np.isfinite(r) & (r != 0)


def resolves(a, b, fmt):
    """True where a and b remain distinct after rounding."""
    return fmt(a) != fmt(b)

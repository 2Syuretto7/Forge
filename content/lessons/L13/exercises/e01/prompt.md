# Rounding to any format

Implement `round_to_format(x, exp_bits, man_bits)` for an array of float64 values: round each to the nearest number representable with `exp_bits` exponent bits and `man_bits` mantissa bits in the IEEE layout, ties to even, including subnormals; values beyond the largest finite number become $\pm\infty$.

The tests compare your fp16 (5, 10) rounding with NumPy's `astype(np.float16)` on thousands of values across the whole range.

## Hints

1. Exponent $e = \lfloor \log_2 |x| \rfloor$, but never below $1 - \text{bias}$ (the subnormal range shares the smallest normal spacing).
2. With $\text{ulp} = 2^{e - m}$, `np.round(|x| / ulp) * ulp` rounds to the grid; `np.round` breaks ties to even.
3. Compare the result with the largest finite value $(2 - 2^{-m}) \cdot 2^{e_{\max}}$ to detect overflow.

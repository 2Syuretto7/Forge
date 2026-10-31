# Decoding a float32

A float32 is 32 bits: 1 sign bit $s$, 8 exponent bits $e$, and 23 fraction bits $f$ (Section 1). For $0 < e < 255$ its value is $(-1)^s (1 + f/2^{23})\,2^{e - 127}$; for $e = 0$ it is subnormal, $(-1)^s f\,2^{-149}$; $e = 255$ holds infinities and NaNs.

- `float32_bits(x)`: the 32-bit integer that stores `x` rounded to float32.
- `decode(bits)`: the tuple `(sign, exponent, fraction, value)`, with `value` a Python float, `inf` or `-inf` for $e = 255$ and $f = 0$, and `nan` for $e = 255$ and $f \ne 0$.
- `spacing(x)`: the gap between the float32 nearest to `x` and the next larger float32.

## Hints

1. `struct.unpack(">I", struct.pack(">f", x))[0]` reads the bits.
2. Shifts and masks: `bits >> 31`, `(bits >> 23) & 0xFF`, `bits & 0x7FFFFF`.
3. `np.spacing(np.float32(x))`, or compute $2^{e - 127 - 23}$ yourself.

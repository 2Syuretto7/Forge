# Emulating bf16, fp16 and fp8 mantissas

Lower-precision formats keep fewer fraction bits: bf16 keeps 7 of float32's 23, fp16 keeps 10, and fp8 E4M3 keeps 3 (L17 uses all three). Emulate the rounding of the fraction in float32 by integer operations on the bits:

- `round_mantissa(x, bits)`: round every float32 in `x` to `bits` fraction bits, to nearest with ties to even. With $k = 23 - \text{bits}$, view the array as `uint32`, add $2^{k-1} - 1 + (\text{the lowest kept bit})$, and clear the low $k$ bits. Return float32. (The exponent range is left alone; only the precision changes.)
- `max_relative_error(bits)`: $2^{-(\text{bits} + 1)}$, the unit roundoff of that precision.
- `accumulate(increment, steps, bits)`: add `increment` to a running total `steps` times, rounding the total to `bits` fraction bits after every addition; return the total.

The tests check the error bound on a million random values, the ties-to-even rule, and why mixed-precision training keeps its running sums in float32: a bf16 accumulator stops growing long before the truth.

## Hints

1. `u = x.view(np.uint32)`; the lowest kept bit is `(u >> k) & 1`.
2. Use `np.uint32` constants so nothing becomes a signed or 64-bit integer.
3. In bf16, the gap between floats near 1 is $2^{-7}$: adding $10^{-3}$ to a total of 1 changes nothing.

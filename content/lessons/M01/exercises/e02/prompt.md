# Scientific notation

Write numbers as a mantissa between 1 and 10 times a power of ten, as in Section 3.

- `to_scientific(x)` returns a pair `(m, e)` with `x == m * 10 ** e`, `1 <= abs(m) < 10` and `e` an integer. For zero return `(0.0, 0)`.
- `from_scientific(m, e)` returns the number `m * 10 ** e` as a float.
- `format_scientific(x, digits)` returns a string such as `"3.00 x 10^8"` with `digits` significant figures (so `digits - 1` decimals in the mantissa).

Python's `math` module has `math.log10` and `math.floor`. The exponent is `floor(log10(abs(x)))`, but floating-point rounding can make `log10` land a hair below a whole number (for example on `1e23`), so check the mantissa afterwards and fix it if it came out as 10 or more, or below 1. Rounding the mantissa for display can also produce 10 (9.996 to three figures is 10.0); renormalize after rounding too.

The tests include an **invariant**: converting to scientific notation and back returns the number you started with, for thousands of random numbers of every size and sign.

## Hints

1. `e = math.floor(math.log10(abs(x)))`, then `m = x / 10 ** e`.
2. If `abs(m) >= 10`, divide `m` by 10 and add 1 to `e`; if `abs(m) < 1`, do the opposite.
3. `f"{m:.2f}"` formats a number with two decimals.

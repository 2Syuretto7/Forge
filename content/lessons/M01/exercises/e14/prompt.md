# Money in floating point

Add prices three ways and compare.

- `sum_floats(amounts)` adds the amounts in order as ordinary Python floats (64-bit), starting from `0.0`.
- `sum_float32(amounts)` adds them in order in 32-bit floats: `np.cumsum(np.asarray(amounts, dtype=np.float32), dtype=np.float32)` gives every running total; return the last one as a Python float.
- `sum_cents(amounts)` converts each amount to a whole number of cents with `round(a * 100)`, adds those integers, and returns the integer total in cents.

Then `drift_cents(amounts)` returns how far `sum_float32` is from the exact total, in cents: `abs(sum_float32(amounts) * 100 - sum_cents(amounts))`.

The tests add a cent a million times. Predict how many cents 32-bit floats lose before you run it.

## Hints

1. `total = 0.0`, then `for a in amounts: total += a`.
2. `float(np.cumsum(...)[-1])`.
3. `round` returns an int when called with one argument, so `sum(round(a * 100) for a in amounts)` is exact.

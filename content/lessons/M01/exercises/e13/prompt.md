# Integers that wrap around

A signed 32-bit integer holds values from $-2^{31}$ to $2^{31} - 1$. Arithmetic past the ends wraps around modulo $2^{32}$, silently.

- `wrap_int32(n)` returns what a 32-bit integer holds after computing the exact integer `n`: shift `n` up by $2^{31}$, take the remainder modulo $2^{32}$, and shift back down.
- `overflows_int32(a, b)` returns `True` when the exact sum `a + b` falls outside the int32 range.
- `numpy_sum_int32(values)` returns the sum NumPy computes for the values stored as 32-bit integers, `np.array(values, dtype=np.int32).sum(dtype=np.int32)`, converted to a Python `int`.

Python's own integers never overflow, so you can compute the exact answer and compare.

## Hints

1. `((n + 2 ** 31) % 2 ** 32) - 2 ** 31`.
2. The range is `-2 ** 31 <= s <= 2 ** 31 - 1`.
3. `int(...)` converts a NumPy integer to a Python one.

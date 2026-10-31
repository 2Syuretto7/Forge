# Machine epsilon and the stall point

- `machine_epsilon(dtype)`: start from `eps = dtype(1)` and halve while `dtype(1) + eps / dtype(2) != dtype(1)`; return the last `eps` as a Python float. It is the gap between 1 and the next float.
- `unit_roundoff(dtype)`: half of it, the largest relative error of rounding to nearest.
- `stall_point(dtype)`: the smallest power of two $N$ with $N + 1 = N$ in that type, found by doubling. Past it, adding 1 does nothing.

The tests check float16, float32 and float64 against the formats' mantissa widths (Section 2).

## Hints

1. Keep every quantity in the given type: `dtype(1) + eps / dtype(2)` with NumPy scalars stays in that type.
2. A format with $p$ stored fraction bits has epsilon $2^{-p}$ and stall point $2^{p + 1}$.
3. `np.finfo(dtype).eps` is a check, not the answer.

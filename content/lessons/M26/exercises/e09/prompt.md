# Comparing floats: units in the last place

`0.1 + 0.2 == 0.3` is false. Equality is the wrong question for computed floats; the right one is how many representable numbers lie between them.

- `ulps_between(a, b)`: the number of float64 steps from `a` to `b`. Map each float to an integer that preserves order: view its bits as a signed 64-bit integer, `i = np.float64(x).view(np.int64)`, and for negative floats use `-(i & 0x7FFFFFFFFFFFFFFF)` instead, so that the integers are ordered like the floats and both zeros map to 0.
- `close(a, b, rel=1e-9, abs_tol=0.0)`: `abs(a - b) <= max(rel * max(abs(a), abs(b)), abs_tol)`, like `math.isclose`.
- `relative_error(approx, exact)`.

## Hints

1. Adjacent floats differ by exactly 1 in this integer order, across the powers of two and across zero.
2. A relative tolerance fails near 0: `close(1e-20, 0.0)` is false unless you give an absolute tolerance.
3. `np.nextafter(x, np.inf)` is the next float above `x`.

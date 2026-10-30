# Where the exponential overflows

- `overflow_threshold(dtype)`: the largest $x$ whose $e^x$ is finite in that NumPy float type, from the formula $\ln(\text{largest finite value})$: `np.log(np.finfo(dtype).max)` computed in float64.
- `first_overflow(dtype)`: the smallest integer $n \geq 0$ for which `np.exp(np.array(n, dtype=dtype))` is infinite, found by trying $n = 0, 1, 2, \dots$ (inside `np.errstate(over="ignore")`).
- `safe_range(dtype)`: the pair `(lo, hi)` of the integers with $e^n$ finite and nonzero: `hi` is one below `first_overflow`, and `lo` is the smallest integer $n$ whose $e^n$ is still above zero in that type (try downward from 0).

## Hints

1. `np.finfo(np.float32).max` is about $3.4 \times 10^{38}$.
2. `np.isinf(...)` tests for infinity.
3. Subnormal numbers let $e^n$ stay above zero a little below the normal range; the loop finds the true edge.

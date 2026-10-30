# 200 choose 100

- `comb_float_factorials(n, k)`: $\binom{n}{k}$ computed as `float(math.factorial(n)) / (float(math.factorial(k)) * float(math.factorial(n - k)))`. For large $n$ the conversion to float raises `OverflowError`; let it.
- `largest_float_factorial()`: the largest $n$ whose $n!$ converts to a finite float.
- `comb_logs(n, k)`: $\binom{n}{k}$ as a float via `math.exp` of log-gamma values (no huge intermediate).
- `comb_exact(n, k)`: exact, with `math.comb`.

The tests show the factorial route failing at $n = 200$ while the log route matches the exact value to many digits.

## Hints

1. `math.factorial(n)` is an exact integer; `float()` of it overflows above about $1.8 \times 10^{308}$.
2. Try $n = 1, 2, \dots$ until `float(math.factorial(n))` raises.
3. `math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))`.

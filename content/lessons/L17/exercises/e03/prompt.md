# Spacing between numbers

1. `ulp(x, exp_bits=5, man_bits=10)`: the spacing of representable numbers at $|x|$, $2^{\lfloor \log_2 |x| \rfloor - m}$, never below the subnormal spacing.
2. `largest_exact_integer(man_bits)`: every integer up to $2^{m+1}$ is exactly representable; return that bound.

Then check: in fp16, $2048 + 1$ rounds back to 2048, and in bf16 the update $1 + 0.001$ rounds back to 1.

## Hints

1. Clamp the exponent at $1 - \text{bias}$.
2. `np.float16(2048) + np.float16(1)` shows the effect directly.
3. A relative change smaller than half the epsilon always rounds away.

# Break it: range against precision

Your `round_to_format` is provided.

1. `bf16(x)` and `fp16(x)`: round to bfloat16 (8, 7) and float16 (5, 10).
2. `survives(x, fmt)`: `True` where a value is finite and nonzero after rounding with `fmt`.
3. `resolves(a, b, fmt)`: `True` where `a` and `b` remain different after rounding.

Then find values that each format loses: large activations, tiny gradients, and small differences between nearby numbers.

## Hints

1. `fmt` is one of your two functions.
2. fp16 loses values above 65504 and below about $6 \times 10^{-8}$; bf16 reaches $10^{\pm 38}$.
3. Near 1, bf16 can only distinguish differences of about 0.008.

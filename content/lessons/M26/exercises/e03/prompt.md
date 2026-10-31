# The order of a sum matters

Floating-point addition is not associative: $(a + b) + c$ and $a + (b + c)$ can differ, because each addition rounds. Sum the harmonic series $\sum_{k=1}^{n} 1/k$ in float32 three ways, with $n = 10^6$:

- `harmonic_terms(n)`: the float32 array $1, \frac12, \dots, \frac1n$.
- `sequential_sum32(x)`: add the entries in the given order, rounding to float32 after every addition.
- `forward(n)` and `backward(n)`: `sequential_sum32` of the terms from large to small, and from small to large.

The true value is $14.392726722865...$. The forward sum stalls: once the total is near 15, a term below half the gap between floats there, $2^{-20}$, rounds away entirely. The backward sum adds the small terms while the total is small.

## Hints

1. `np.cumsum(x, dtype=np.float32)` adds sequentially in float32; its last entry is the sum.
2. Reverse with `x[::-1]`.
3. `np.sum` is not sequential: NumPy adds in blocks and pairs, which is more accurate. Do not use it here.

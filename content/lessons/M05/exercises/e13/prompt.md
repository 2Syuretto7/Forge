# Summation order in float32

Add $\sum_{k=1}^{10^6} 1/k^2$ in 32-bit floating point, in both orders. The exact sum (to float64 accuracy) is `np.sum(1 / k**2)` computed in float64.

- `terms(n)`: the float32 array of $1/k^2$ for $k = 1, \dots, n$ (compute in float64, then convert).
- `forward(t)`: the running total added from the first term to the last, in float32. `np.cumsum(t, dtype=np.float32)[-1]` adds strictly in order.
- `backward(t)`: the same from the last term to the first.
- `errors(n)`: the pair `(forward_error, backward_error)` against the float64 sum of the same terms.

Predict which error is larger, and by how much, before you run it.

## Hints

1. `(1 / np.arange(1, n + 1, dtype=np.float64) ** 2).astype(np.float32)`.
2. `t[::-1]` reverses an array.
3. Use the float64 sum of the float32 terms as the reference, so you measure only the adding.

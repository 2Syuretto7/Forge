# Naive softmax returns nan

Work in NumPy, which does not raise on overflow; it returns infinities and nan.

- `naive_softmax(z)`: `np.exp(z) / np.exp(z).sum()` for a float64 array, inside `np.errstate(all="ignore")` so it fails silently.
- `stable_softmax(z)`: the same after subtracting `z.max()`.
- `fails(z)`: `True` when the naive version produces any nan or infinity.
- `smallest_failing_shift(z)`: the smallest integer `c` such that `naive_softmax(z + c)` fails, trying `c = 0, 1, 2, ...` up to 1,000. For scores near 0 this is about 710, the float64 overflow threshold.

## Hints

1. `with np.errstate(all="ignore"): e = np.exp(z)`.
2. `not np.all(np.isfinite(p))`.
3. Shifting every score by `c` never changes the true softmax; it only moves the computation toward overflow.

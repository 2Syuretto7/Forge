# Sums that stop growing

1. `naive_sum(values, dtype)`: add the values one at a time, rounding the running sum to `dtype` after every addition.
2. `kahan_sum(values, dtype)`: compensated summation, also entirely in `dtype`: keep a correction `c` holding the rounding error of the last addition and subtract it from the next input.
3. `wide_accumulator_sum(values, dtype)`: store the inputs in `dtype` but add them up in float32.

Sum ten thousand copies of 0.01 in fp16 with each.

## Hints

1. Wrap every intermediate in `dtype(...)` so NumPy does not silently use a wider type.
2. Kahan: `y = v - c; t = s + y; c = (t - s) - y; s = t`.
3. The true sum is 100; the naive fp16 sum stops at 32.

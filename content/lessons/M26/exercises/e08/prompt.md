# Compensated summation, vectorized

Summing $n$ numbers one after another accumulates a rounding error that can grow like $n\varepsilon$ (Section 6). Two remedies:

- **Pairwise** summation adds neighbours in pairs, then pairs of pairs: each number passes through only $\log_2 n$ additions, and the error grows like $\varepsilon\log n$.
- **Kahan** summation carries the rounding error of each addition in a compensation term $c$ and feeds it back: with $y = x - c$, $t = s + y$, $c = (t - s) - y$, $s = t$, the error stays near $\varepsilon$ whatever $n$ is.

Implement, all in float32:

- `naive_sum32(x)`: sequential, as in e03.
- `pairwise_sum32(x)`: repeatedly add even and odd entries, `x[0::2] + x[1::2]`, padding with a zero when the length is odd, until one number remains.
- `kahan_sum32(x, width=10000)`: run Kahan's loop on `width` independent running sums at once, one row of a `(rows, width)` array at a time (pad with zeros to fill the last row), then add the `width` totals with the same compensated loop, one at a time.

The tests sum a million copies of `np.float32(0.1)`.

## Hints

1. Keep every array and scalar in float32; a single float64 sneaks the whole computation into double precision.
2. The vectorized Kahan loop is four array operations per row, all of length `width`.
3. Exact reference: `float(np.sum(x.astype(np.float64)))`; each float32 is exactly a float64.

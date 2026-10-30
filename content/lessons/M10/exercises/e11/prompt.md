# How time grows with size

- `time_matmul(n, repeats=3, seed=0)`: the fastest of `repeats` timings of one float64 `(n, n) @ (n, n)` product.
- `fit_exponent(ns, times)`: the slope of the least-squares line through the points $(\log n, \log t)$. If time grows like $n^k$, the slope is $k$.
- `predicted_ratio(n1, n2)`: $(n_2 / n_1)^3$, the ratio the operation count predicts.

On small matrices overheads hide the cube law, so measure from about 128 upward. Expect a measured exponent between 2 and 3.5: modern libraries keep the arithmetic units busier on larger matrices.

## Hints

1. `min(...)` of several timings removes most interruptions.
2. `np.polyfit(np.log(ns), np.log(times), 1)[0]`.
3. Test `fit_exponent` on exact powers before trusting it on measurements.

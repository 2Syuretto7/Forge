# Measuring the rate

- `observed_rate(residuals)`: the typical ratio of successive residuals over the second half of the list (the median of `r[k+1] / r[k]`), which estimates $|\lambda_2|$ of the iteration.
- `predicted_steps(rate, tol, r0)`: the number of steps for a residual starting at `r0` to fall below `tol` at that rate, $\lceil \ln(\text{tol}/r_0) / \ln(\text{rate}) \rceil$.

The starter provides `make_graph` and `pagerank_sparse` from e10. The damping factor bounds the rate: $|\lambda_2| \leq d$. Measure the rate for $d$ = 0.5, 0.85 and 0.95 and compare.

## Hints

1. `np.median(np.array(r[1:]) / np.array(r[:-1]))` over the tail.
2. On a synthetic list $r_k = 0.5^k$ the rate is exactly 0.5.
3. The prediction counts steps after the first residual.

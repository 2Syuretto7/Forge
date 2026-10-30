# Reading growth from doubling

If a cost behaves like $C n^p$, doubling $n$ multiplies it by $2^p$, whatever $C$ is.

- `doubling_ratio(cost, n)`: `cost(2 * n) / cost(n)`.
- `exponent_estimate(cost, n)`: $\log_2$ of that ratio.
- `classify(cost, n=1024)`: one of `"constant"`, `"logarithmic"`, `"linear"`, `"n log n"`, `"quadratic"`, `"cubic"` or `"exponential"`, decided from the doubling ratio at `n`: about 1 is constant; slightly above 1 (below 1.2) logarithmic; about 2 linear; between 2.05 and 2.4 n log n; about 4 quadratic; about 8 cubic; far larger exponential.

## Hints

1. `math.log2(r)`.
2. Check the bands in order; for $n \log n$ at $n = 1024$ the ratio is $2 \cdot \frac{11}{10} = 2.2$.
3. An exponential cost $2^n$ has ratio $2^n$ at doubling, astronomically large.

# Break it: the one-pass variance formula

$\operatorname{Var}X = \mathbb{E}X^2 - (\mathbb{E}X)^2$ is exact algebra and terrible arithmetic: when the mean is large compared with the spread, both terms are huge and nearly equal, and their difference is rounding noise (Section 3).

- `one_pass_var(x)`: $\frac{1}{n}\sum x_i^2 - \bar x^2$, accumulated in the array's own dtype.
- `two_pass_var(x)`: the mean first, then the mean squared deviation.
- `welford_var(x)`: one pass, updating a running mean $m$ and sum of squared deviations $M$: for the $k$-th value, $\delta = x - m$, $m \leftarrow m + \delta/k$, $M \leftarrow M + \delta(x - m)$; return $M/n$. Loop over Python floats.

The tests use timestamps near $1.7 \times 10^9$ seconds with a spread of 1 second in float64, and readings near 10,000 with a spread of 1 in float32. In both the one-pass formula returns rounding noise: the squares are so large that the gap between neighbouring floats exceeds the variance itself.

## Hints

1. Keep the dtype: `np.mean(x * x) - np.mean(x) ** 2` with a float32 `x` computes in float32.
2. Welford's update needs no large intermediate: it only ever squares deviations.
3. A negative variance is the clearest sign: no data can have one.

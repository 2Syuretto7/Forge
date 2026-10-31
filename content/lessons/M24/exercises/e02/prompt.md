# The law of large numbers, watched

- `running_mean(x)`: the array of averages of the first $1, 2, \dots, n$ entries.
- `fraction_far(samples, mu, eps)`: `samples` has shape `(trials, n)`; the fraction of rows whose mean misses $\mu$ by more than $\varepsilon$.
- `chebyshev_n(var, eps, delta)`: the smallest $n$ for which Chebyshev guarantees $P(\lvert\bar x - \mu\rvert \ge \varepsilon) \le \delta$, that is $n \ge \sigma^2/(\varepsilon^2\delta)$.

The tests watch the fraction of far-off averages of fair coin flips fall as $n$ grows, always below Chebyshev's guarantee, and usually far below.

## Hints

1. `np.cumsum(x) / np.arange(1, len(x) + 1)`.
2. `np.mean(np.abs(samples.mean(axis=1) - mu) > eps)`.
3. `math.ceil`, and guard against floating-point fuzz such as `50000.00000001` with a small rounding first.

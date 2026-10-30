# Measure your browser's matrix throughput

Estimate, then measure. Time NumPy's matrix product and convert the time into FLOPs per second.

- `time_matmul(n, min_time=0.02)` builds two random $n \times n$ matrices, multiplies them repeatedly, and returns the seconds per multiplication. A browser's clock ticks coarsely (often once per millisecond), so a single product is too fast to time: start with one repetition and double the count until a batch takes at least `min_time` seconds, then divide.
- `flops_per_second(n)` returns $2n^3$ divided by `time_matmul(n)`: an $n \times n$ by $n \times n$ product is $n^2$ outputs, each $n$ multiply-adds.
- `predict_seconds(n, rate)` returns $2n^3 / \text{rate}$.

Use `time.perf_counter()` for the clock: it returns seconds as a float.

## Hints

1. `A = np.random.default_rng(0).normal(size=(n, n))`.
2. Inside a `while True:` loop, time `reps` products; if the batch took at least `min_time`, return `elapsed / reps`; otherwise `reps *= 2`.
3. A matrix product of $n \times n$ matrices is $n^2 \times n$ multiply-adds.

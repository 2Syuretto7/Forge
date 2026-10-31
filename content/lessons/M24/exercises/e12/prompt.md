# Running the one-in-a-million estimate

Put e10's numbers to work. The starter provides `upper_tail` and `best_shift` from e10.

- `naive_hits(a, n, rng, chunk=10**6)`: draw `n` standard normals in chunks and count how many exceed `a`.
- `is_rare(a, theta, n, rng)`: draw `n` samples from $N(\theta, 1)$ with one call `theta + rng.standard_normal(n)`, weight them by $e^{-\theta x + \theta^2/2}$, and return the estimate of $P(Z > a)$ and its standard error.

The tests give the naive sampler four million draws, a few dozen times more than the importance sampler's hundred thousand, and see it find a handful of hits, while the importance sampler lands within 2 percent of $10^{-6}$.

## Hints

1. Loop `while done < n`, drawing `min(chunk, n - done)` at a time.
2. The estimate is the mean of `(x > a) * w`.
3. With $P = 10^{-6}$, four million draws expect four hits: a relative error of 50 percent.

# Break it: one test set, a thousand models

Pick the best of 1,000 models by their accuracy on one test set of 1,000 examples, then report that accuracy with a Hoeffding interval as if it were a single model's. If every model actually guesses at random, the true accuracy is $0.5$, the reported one is about $0.55$, and the interval misses the truth (Section 2).

- `select_and_report(k, n, rng, delta=0.05)`: simulate $k$ random-guessing models on one test set, select the best, and return `(reported, low, high)` with the single-model Hoeffding half-width.
- `fresh_accuracy(n, rng)`: the selected model's accuracy on a fresh test set; since it guesses at random, draw it the same way.
- `honest_interval(reported, n, k, delta=0.05)`: the interval with the union-bound half-width $\sqrt{\ln(2k/\delta)/(2n)}$.

The tests find the naive interval excluding $0.5$ in nearly every run, while the honest interval includes it, and the fresh accuracy back near $0.5$.

## Hints

1. Reuse e04's simulation.
2. The selection happened after looking at the test set: the reported number is the maximum of 1,000 noisy estimates, not one estimate.
3. The repair costs only $\sqrt{\ln k}$: a thousand models need about 1.7 times the half-width of one.

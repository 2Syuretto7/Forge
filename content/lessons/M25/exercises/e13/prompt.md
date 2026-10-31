# Bootstrapping 100,000 examples, 2,000 times

A model is evaluated on 100,000 examples and you want a bootstrap interval for its accuracy, from 2,000 resamples. Resampling indices takes $2 \times 10^8$ integers, 1.6 GB. But the mean of a resample depends only on how many times each **distinct value** was drawn, and those counts follow a multinomial distribution.

- `bootstrap_by_index(values, B, rng)`: the plain bootstrap of e11, with `rng.integers(0, n, size=(B, n))`, for small data.
- `bootstrap_by_counts(values, B, rng)`: find the distinct values and their counts with `np.unique`, draw `rng.multinomial(n, counts / n, size=B)`, and return the `B` resample means.
- `paired_interval(correct_a, correct_b, B, rng, level=0.95)`: two models scored on the same examples, 0 or 1 each; bootstrap the per-example difference `correct_b - correct_a` (values $-1$, 0, 1) by counts and return the percentile interval of the mean difference.

The tests check that both bootstraps agree on small data, run the fast one at full size, and show the paired interval much narrower than the interval you would get by treating the two accuracies as independent.

## Hints

1. `u, c = np.unique(values, return_counts=True)`, then `M @ u / n` where `M` holds the multinomial counts.
2. For 0/1 values there are two distinct values, and the multinomial reduces to a binomial.
3. Models that agree on most examples have differences that are mostly 0: pairing removes the shared difficulty of the examples.

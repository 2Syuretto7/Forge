# Binomial and Poisson samplers from simpler pieces

Section 4 builds two families from simpler ones. Implement both constructions with the generator `rng` you are given.

- `binomial_by_sum(n, p, size, rng)`: `size` samples, each the number of successes in `n` Bernoulli(`p`) trials.
- `poisson_by_arrivals(lam, size, rng)`: `size` samples, each the number of arrivals before time `lam` when the gaps between arrivals are independent Exponential(1) variables, drawn as $-\log(1 - U)$ from `rng.random`.
- `moments(x)`: the sample mean and the sample variance (dividing by $n - 1$) of an array.

The tests compare both samplers' moments with the table: $np$ and $np(1-p)$, $\lambda$ and $\lambda$.

## Hints

1. `(rng.random((size, n)) < p).sum(axis=1)`.
2. For arrivals, keep a running time per sample and a count, and loop while any sample's time is still below `lam`; add a new gap only to those samples.
3. `np.var(x, ddof=1)`.

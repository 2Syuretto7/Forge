# A Monte Carlo simulator

- `simulate(trial, n, seed=0)`: run `trial(rng)` `n` times with one `random.Random(seed)` passed to every call, and return the fraction of runs that returned `True`.
- `standard_error(p, n)`: $\sqrt{p(1 - p)/n}$, the typical size of the gap between a simulated fraction and the true probability $p$.
- `z_score(estimate, p, n)`: the gap measured in standard errors.
- `roll_two_sum_seven(rng)`: one trial: roll two dice with `rng.randint(1, 6)` and report whether they sum to 7.

A simulation agrees with an exact answer when the z-score is within about 3. M24 proves why.

## Hints

1. `sum(trial(rng) for _ in range(n)) / n`.
2. `math.sqrt(p * (1 - p) / n)`.
3. `(estimate - p) / standard_error(p, n)`.

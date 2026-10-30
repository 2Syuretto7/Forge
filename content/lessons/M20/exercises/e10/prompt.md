# The vanishing ball

- `ball_volume(n)`: $\pi^{n/2} / \Gamma(n/2 + 1)$ with `math.gamma`.
- `cube_fraction(n)`: $V_n / 2^n$.
- `mc_fraction(n, samples, seed=0)`: the fraction of uniform points of $[-1, 1]^n$ inside the unit ball, with its standard error.
- `peak_dimension(max_n=50)`: the dimension with the largest ball volume.

The tests check the sampling against the formula up to 10 dimensions and find the peak at $n = 5$.

## Hints

1. `rng.uniform(-1, 1, size=(samples, n))`, then the squared norms of the rows.
2. The standard error of a fraction $p$ from $N$ samples is $\sqrt{p(1 - p)/N}$.
3. Loop over $n$ from 1 to `max_n`.

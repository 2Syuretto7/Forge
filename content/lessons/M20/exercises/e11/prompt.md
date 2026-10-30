# Where a high-dimensional ball keeps its volume

- `shell_fraction(n, eps)`: the fraction of the unit ball's volume within distance `eps` of its surface, $1 - (1 - \varepsilon)^n$.
- `sample_ball(n, m, seed=0)`: `m` points uniform in the unit ball of $\mathbb{R}^n$: a random direction (a normalized standard normal vector) times a radius $U^{1/n}$, where $U$ is uniform.
- `mean_radius(n, m=100_000, seed=0)`: the average distance from the centre of `sample_ball` points; it is $n/(n + 1)$.

The radius $U^{1/n}$ comes from the change of variables: the volume within radius $r$ is proportional to $r^n$, so $P(R \leq r) = r^n$, and inverting the distribution function gives $R = U^{1/n}$.

## Hints

1. In 100 dimensions, 99.3 percent of the volume lies within 0.05 of the surface.
2. Normalize the rows of a Gaussian matrix.
3. `rng.random(m) ** (1 / n)`.

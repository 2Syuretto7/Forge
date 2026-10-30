# Box-Muller

- `box_muller(u1, u2)`: arrays `(x, y)` from arrays of uniforms in $(0, 1]$: $\sqrt{-2\ln u_1}\,(\cos 2\pi u_2, \sin 2\pi u_2)$.
- `sample_normal(n, seed=0)`: `n` standard normals, using both outputs of each pair.
- `check_moments(z)`: `(mean, variance, fraction within one standard deviation)`.

For a standard normal, the fraction within one standard deviation is $\operatorname{erf}(1/\sqrt 2) \approx 0.6827$.

## Hints

1. Draw `u1` as `1 - rng.random(m)` so that it is never 0.
2. `np.concatenate([x, y])[:n]`.
3. `np.mean(np.abs(z) < 1)`.

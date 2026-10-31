# Steps and schedules

How many steps does the reverse process need, and where should they go (Section 7)? Measure the quality of 4,000 one-dimensional samples, generated with the exact score of e05's mixture, as the number of steps varies, for two time grids: uniform in $t$, and geometric, which crowds the steps near $t = 0$.

- `uniform_grid(T, steps, tmin=1e-3)` and `geometric_grid(T, steps, tmin=1e-3)`.
- `sample_on_grid(score, n, grid, rng)`: e07's reverse steps over an arbitrary decreasing grid.
- `quality(score, data, grids, n, rng)`: the list of $W_1$ distances of samples generated on each grid from `data`.

The tests find the error falling with the number of steps for both grids, and the geometric grid with 20 steps beating the uniform one with 20 steps by a wide margin.

## Hints

1. Reuse e07's `w1`, with equal sample sizes.
2. Near $t = 0$ the noised density is nearly the data density, whose narrow components make the score change fast; far from 0 everything is smooth and nearly Gaussian.
3. Production samplers use carefully designed time grids and higher-order solvers for exactly this reason.

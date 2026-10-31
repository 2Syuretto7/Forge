# A grid against random points in eight dimensions

Integrate $f(x) = e^{-\lVert x\rVert^2}$ over the cube $[0, 1]^d$, whose exact value is $c^d$ with $c = \int_0^1 e^{-t^2}dt \approx 0.746824$, two ways with the same number of points.

- `grid_mean(f, d, k)`: the midpoint rule, the average of $f$ over the $k^d$ points whose coordinates are $(i + \frac12)/k$; `f` takes an `(m, d)` array and returns `m` values.
- `mc_mean(f, d, n, rng)`: the average of $f$ over `rng.random((n, d))`.

In one dimension 1,000 grid points beat 1,000 random ones by a factor of ten thousand. In eight dimensions the same budget, $4^8 = 65{,}536$ points, gives the grid only 4 points per axis, and random points win.

## Hints

1. `pts = (np.arange(k) + 0.5) / k`, then `np.stack(np.meshgrid(*[pts] * d, indexing="ij"), axis=-1).reshape(-1, d)`.
2. The midpoint rule's error per axis falls like $1/k^2$, but $k = n^{1/d}$: in $d$ dimensions it falls like $n^{-2/d}$.
3. Monte Carlo's error falls like $n^{-1/2}$ in every dimension.

# Turn once or turn many times

Turning by $k\delta$ can be done in one step, or as $k$ steps of $\delta$. In exact arithmetic they agree.

- `turn_direct(points, k, delta)`: one rotation by `k * delta` (float64).
- `turn_repeated(points, k, delta)`: `k` rotations by `delta` (float64).
- `gap(points, k, delta)`: the largest absolute difference between the two.
- `gap_growth(points, ks, delta)`: the list of gaps for each `k` in `ks`.

The tests check that the gap grows with `k` roughly in proportion (rounding errors accumulate one step at a time) while staying near rounding level.

## Hints

1. Reuse a row-vector rotation matrix as in the previous exercise.
2. The direct turn computes $\cos(k\delta)$ once; the repeated turn rounds $k$ times.
3. A list comprehension over `ks`.

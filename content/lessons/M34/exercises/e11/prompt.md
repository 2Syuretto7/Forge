# Distances concentrate too

In high dimension not only norms but distances between random points concentrate: for $n$ points uniform in the cube $[0, 1]^d$, the farthest and the nearest point from a query differ by a vanishing fraction of the distance as $d$ grows (Section 1). Nearest-neighbour search on raw high-dimensional data loses its meaning unless the data have low-dimensional structure.

- `relative_contrast(d, n, rng, queries=20)`: average, over `queries` random query points, of $(\text{max distance} - \text{min distance})/\text{min distance}$ to $n$ uniform points.
- `expected_sq_distance(d)`: $\mathbb{E}\lVert x - y\rVert^2 = d/6$ for independent uniform points.
- `distance_cv(d, n, rng)`: the coefficient of variation (standard deviation over mean) of distances between independent pairs, which falls like $1/\sqrt d$.

The tests find the contrast falling from more than 10 in 2 dimensions to below 0.5 in 1,000, and the mean squared distance matching $d/6$.

## Hints

1. Each coordinate contributes $\mathbb{E}(x_i - y_i)^2 = 1/6$ for independent uniforms.
2. Compute the distances from one query to all points with `np.linalg.norm(P - q, axis=1)`.
3. The squared distance is a sum of $d$ independent terms, so its relative spread falls like $1/\sqrt d$, exactly as the norm's did in e01.

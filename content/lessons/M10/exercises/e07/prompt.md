# Areas scale by the determinant

- `polygon_area(P)`: the signed area of the polygon with vertices the rows of `P`, by the shoelace formula $\frac12 \sum_i (x_i y_{i+1} - x_{i+1} y_i)$ (indices wrap around); positive when the vertices run counterclockwise.
- `area_ratio(M, P)`: the signed area of the image polygon divided by that of `P`.

The tests check an **invariant**: for random polygons and random matrices, `area_ratio(M, P)` equals $\det M$, sign included, so a reflection turns a counterclockwise polygon clockwise.

## Hints

1. `np.roll(P, -1, axis=0)` lines up each vertex with the next.
2. Map the points with `P @ M.T`.
3. A random polygon: points at sorted random angles around the origin, at random radii.

# Polar coordinates, and pi from polygons

- `to_polar(x, y)` and `to_cartesian(r, theta)`, as pairs.
- `regular_polygon(n, r=1.0)`: the $n$ vertices of a regular polygon inscribed in a circle of radius `r`, at angles $2\pi k / n$.
- `perimeter(points)`: the length of the closed path through the points in order (back to the first).
- `pi_estimate(n)`: half the perimeter of the regular $n$-gon in the unit circle. Archimedes used a 96-gon to show $3\frac{10}{71} < \pi < 3\frac{1}{7}$; the inscribed polygon gives the lower bound.

## Hints

1. `(math.hypot(x, y), math.atan2(y, x))`.
2. Use your `to_cartesian` for each vertex.
3. Pair each point with the next, wrapping around with `points[(i + 1) % n]`.

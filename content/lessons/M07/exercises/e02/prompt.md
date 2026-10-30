# The unit circle

- `point_on_circle(theta, r=1.0)`: the point $(r\cos\theta, r\sin\theta)$ as a tuple.
- `angle_of(x, y)`: the angle of the point $(x, y)$ in $(-\pi, \pi]$, with `math.atan2(y, x)` (note the order of the arguments).
- `distance(p, q)`: the distance between two points, by Pythagoras.

The tests check an **invariant**: the point at angle $\theta$ has angle $\theta$ (normalized) and distance $r$ from the origin, for thousands of random angles and radii.

## Hints

1. `(r * math.cos(theta), r * math.sin(theta))`.
2. `atan2` handles every quadrant; `atan(y / x)` does not.
3. `math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)`.

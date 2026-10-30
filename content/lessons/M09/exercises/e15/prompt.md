# A distance that is not one

A **metric** $D$ must satisfy the triangle inequality $D(x, z) \leq D(x, y) + D(y, z)$.

- `cosine_distance(x, y)`: $1 - \cos t$.
- `angular_distance(x, y)`: the angle $t$ itself, in radians, with the cosine clipped to $[-1, 1]$.
- `triangle_violation(D, x, y, z)`: $D(x, z) - D(x, y) - D(y, z)$, positive when the triangle inequality fails.
- `find_violation(D, trials=1000, seed=0)`: search random triples of unit vectors in the plane for one with a positive violation; return it (a tuple of three arrays) or `None`.

The tests find a violation for the cosine distance and none for the angular distance.

## Hints

1. Unit vectors in the plane: `np.array([np.cos(a), np.sin(a)])` for random angles.
2. Three vectors at $0^\circ$, $60^\circ$ and $120^\circ$: the cosine distances are $0.5$, $0.5$ and $1.5$.
3. The angle between unit vectors is the arc between them on the circle, which obeys the triangle inequality.

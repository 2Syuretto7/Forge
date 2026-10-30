# Rotations, stretches, shears and reflections

Return 2 by 2 NumPy arrays:

- `rotation(theta)`: turn counterclockwise by `theta` radians.
- `scaling(sx, sy)`: stretch the axes by `sx` and `sy`.
- `shear(k)`: the horizontal shear $(x, y) \mapsto (x + k y, y)$.
- `reflection(phi)`: reflect across the line through the origin at angle `phi`. Its columns are the images of $e_1$ and $e_2$: a direction at angle $\alpha$ reflects to angle $2\phi - \alpha$.

The tests check an **invariant** for random angles: rotations keep every dot product, $R(a) R(b) = R(a + b)$, and reflecting twice changes nothing.

## Hints

1. The columns of `rotation(theta)` are $(\cos\theta, \sin\theta)$ and $(-\sin\theta, \cos\theta)$.
2. $e_1$ is at angle 0 and goes to angle $2\phi$; $e_2$ is at angle $\pi/2$ and goes to $2\phi - \pi/2$.
3. `np.array([[a, b], [c, d]])` has columns `(a, c)` and `(b, d)`.

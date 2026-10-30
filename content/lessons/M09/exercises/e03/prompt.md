# The dot product two ways

Section 3 showed the dot product equals $\|x\|\,\|y\|\cos t$. Check it numerically in a way that does not use the dot product to find the angle.

- `angle_2d(x, y)`: for two vectors in the plane, the angle between them from their individual directions: the difference of `math.atan2(x[1], x[0])` and the same for `y`, brought into $[0, \pi]$.
- `dot_by_angle(x, y)`: $\|x\|\,\|y\|\cos t$ with $t$ from `angle_2d`.
- `law_of_cosines_gap(x, y)`: $\|x - y\|^2 - (\|x\|^2 + \|y\|^2 - 2\,x \cdot y)$ in any dimension, which should be zero up to rounding.

## Hints

1. Take the absolute difference of the two `atan2` angles, then use `2 * pi - d` if it exceeds $\pi$.
2. Lengths with `math.hypot` in two dimensions.
3. Compute each piece directly from coordinates.

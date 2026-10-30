# Renormalize

Fix a rotation matrix whose entries have been rounded, and stop drift that builds up over many steps.

- `renormalize(c, s)`: divide both by $\sqrt{c^2 + s^2}$, so the matrix is a true rotation again.
- `turn_with_renormalization(c, s, steps)`: apply the renormalized matrix `steps` times to $(1, 0)$ and return the final point.
- `angle_error(c, s, theta)`: how far (in radians) the angle of the renormalized matrix, $\operatorname{atan2}(s, c)$, is from the intended `theta`. Renormalizing fixes the length but not the angle: rounding moved the angle a little, and that error grows linearly with the number of steps instead of geometrically.

## Hints

1. `r = math.hypot(c, s); return c / r, s / r`.
2. Reuse the rotation loop of the previous exercise.
3. `abs(math.atan2(s, c) - theta)`.

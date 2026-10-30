# Degrees and radians

- `to_radians(deg)` and `to_degrees(rad)`: a full turn is 360 degrees and $2\pi$ radians.
- `normalize(theta)`: the equivalent angle in $(-\pi, \pi]$, by adding or subtracting whole turns.
- `same_direction(a, b)`: whether two angles (in radians) point the same way, that is differ by a whole number of turns, to within `1e-9`.

The tests check an **invariant**: converting degrees to radians and back returns the original, and `normalize` never changes $\cos$ or $\sin$ of an angle.

## Hints

1. `deg * math.pi / 180`.
2. `theta - 2 * math.pi * math.ceil((theta - math.pi) / (2 * math.pi))` lands in $(-\pi, \pi]$; check the ends.
3. Normalize the difference and compare it with 0.

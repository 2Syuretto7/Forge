# Rotation by complex multiplication

Python's built-in `complex` type works like your class: `complex(3, 4)`, `z.real`, `z.imag`, `abs(z)`, and `cmath.exp`.

- `rotate_complex(p, theta)`: rotate the point `p = (x, y)` by multiplying $x + iy$ by $\cos\theta + i\sin\theta$; return a tuple.
- `rotate_trig(p, theta)`: rotate with the formula of Section 3.
- `compose_angles(thetas)`: the single complex number that rotates by all the angles in turn, as the product of their unit complex numbers; return its angle.
- `quarter_turns(p, k)`: `p` multiplied by $i$ `k` times, as a tuple.

The tests check that the two rotations agree and that four quarter turns return every point to itself.

## Hints

1. `z = complex(*p) * complex(math.cos(theta), math.sin(theta))`.
2. Multiply the unit numbers together, then use `cmath.phase`.
3. Multiply by `1j` in a loop.

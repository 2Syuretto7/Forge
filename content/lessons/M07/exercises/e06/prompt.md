# The angle-addition formulas, checked

- `cos_sum(a, b)` and `sin_sum(a, b)`: $\cos(a + b)$ and $\sin(a + b)$ computed **only** from $\cos a$, $\sin a$, $\cos b$, $\sin b$ with the formulas of Section 3.
- `double_angle(a)`: the pair $(\cos 2a, \sin 2a)$ from the formulas.
- `half_angle_cos(a)`: $\cos(a/2)$ for $a$ in $[0, \pi]$, from $\cos a = 2\cos^2(a/2) - 1$ (a rearranged double-angle formula), taking the positive root.

The tests compare with `math.cos` and `math.sin` at thousands of angles.

## Hints

1. `math.cos(a) * math.cos(b) - math.sin(a) * math.sin(b)`.
2. `cos_sum(a, a)` and `sin_sum(a, a)`.
3. $\cos(a/2) = \sqrt{(1 + \cos a)/2}$.

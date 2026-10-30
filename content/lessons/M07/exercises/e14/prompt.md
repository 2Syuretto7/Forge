# A rotation that is not quite a rotation

- `rounded_rotation(theta, decimals)`: the pair `(c, s)` of $\cos\theta$ and $\sin\theta$ each rounded to `decimals` places.
- `scale_factor(c, s)`: how much one step with the matrix $\begin{pmatrix} c & -s \\ s & c \end{pmatrix}$ stretches every length: $\sqrt{c^2 + s^2}$.
- `radius_after(c, s, steps)`: the length of the point $(1, 0)$ after `steps` applications, computed by actually applying the matrix in a loop.
- `predicted_radius(c, s, steps)`: the same from the scale factor alone.

The tests round the entries for $\theta = 37^\circ$ to 3 places and apply them 10,000 times.

## Hints

1. `round(math.cos(theta), decimals)`.
2. The matrix is $\sqrt{c^2 + s^2}$ times a true rotation, so every step multiplies lengths by that factor.
3. `scale_factor(c, s) ** steps`.

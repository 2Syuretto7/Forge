# Directional derivatives and steepest ascent

- `directional(grad, x, u)`: $\nabla f(x) \cdot u / \|u\|$, the slope in the direction of `u`.
- `steepest(grad, x)`: the unit vector of steepest ascent.
- `numerical_directional(f, x, u, h=1e-6)`: the central difference of $t \mapsto f(x + t\,u/\|u\|)$ at 0.

The tests run a **gradient check**: the formula agrees with the numerical slope in random directions, never exceeds $\|\nabla f\|$, and reaches it along `steepest`.

## Hints

1. Normalize `u` first.
2. `g / np.linalg.norm(g)`.
3. One central difference along the line, two evaluations.

# Double integrals by Fubini

- `midpoint_2d(f, ax, bx, ay, by, n)`: the midpoint rule on an `n` by `n` grid of the rectangle, for a vectorized `f(x, y)` (use `np.meshgrid`).
- `iterated(f, ax, bx, ay, by, n=200)`: an inner Simpson integral in $y$ for each outer Simpson node in $x$: Fubini as code.
- `over_triangle(f, n=400)`: $\iint_{0 \leq y \leq x \leq 1} f\,dA$ by iterating with the inner limit depending on $x$.

## Hints

1. `X, Y = np.meshgrid(xm, ym, indexing="ij")` for the midpoints, then multiply the sum by the cell area.
2. Write a one-dimensional Simpson helper and call it inside a function of $x$.
3. For the triangle, the inner integral runs from 0 to $x$.

# Random directions are nearly perpendicular

For independent standard normal $x, y \in \mathbb R^d$, the cosine $\frac{x\cdot y}{\lVert x\rVert\lVert y\rVert}$ has mean 0 and variance $1/d$ (Section 2): the dot product is a sum of $d$ independent terms of variance 1, and each length is about $\sqrt d$. The angle is $90°$ give or take about $57.3/\sqrt d$ degrees.

- `cosines(d, pairs, rng)`: the cosines of `pairs` independent pairs.
- `angles_degrees(d, pairs, rng)`: the angles, in degrees.
- `predicted_angle_sd(d)`: $\frac{180}{\pi\sqrt d}$, the small-angle approximation.

The tests answer the puzzle in 4,096 dimensions: mean $90°$, spread about $0.9°$, and not a single pair in 2,000 more than $5°$ from perpendicular.

## Hints

1. `np.einsum("ij,ij->i", X, Y)` computes all the row-wise dot products.
2. `np.degrees(np.arccos(c))`.
3. In 3 dimensions the angles are spread over the whole range, with density proportional to $\sin\theta$.

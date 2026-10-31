# Projected gradient descent

To minimize over a simple set $C$, take a gradient step and project back: $x \leftarrow \Pi_C(x - \eta\nabla f(x))$, where $\Pi_C(y)$ is the closest point of $C$ to $y$ (Section 4). For a convex $f$ and a convex $C$ it converges at the rates of M29.

- `project_box(y, lo, hi)`: clip coordinatewise.
- `project_ball(y, r)`: rescale onto the ball of radius `r` if outside.
- `project_simplex(y)`: the closest point with nonnegative coordinates summing to 1. Sort $y$ in decreasing order, find the largest $k$ with $u_k - \frac1k(\sum_{i \le k}u_i - 1) > 0$, set $\theta = \frac1k(\sum_{i\le k}u_i - 1)$, return $\max(y - \theta, 0)$.
- `projected_gd(grad, proj, x0, step, iters)`: the final iterate.

The tests check each projection's defining property and minimize a quadratic over the simplex.

## Hints

1. A projection is idempotent: projecting twice changes nothing.
2. For the simplex, `np.cumsum` of the sorted values gives every candidate $\theta$ at once.
3. The projection's optimality condition: $(y - \Pi(y))^\top(z - \Pi(y)) \le 0$ for every $z$ in the set.

# A ReLU network built by hand

Section 2 showed how to write any piecewise linear interpolant as a one-hidden-layer ReLU network. Build it explicitly, with no training.

- `hinge_network(knots, values)`: knots $t_0 < \dots < t_k$ and target values there. Return `(w, b, a, c)` for $f(x) = c + \sum_j a_j\,\max(0, w_j x + b_j)$ that equals linear interpolation on $[t_0, t_k]$. Use one unit with $w = 1, b = -t_0$ carrying the first slope, and one unit per interior knot with output weight equal to the change of slope.
- `evaluate(params, x)`.
- `max_error(f, n_pieces)`: for $f$ on $[-1, 1]$ and `n_pieces` equal pieces, build the network from $f$ at the knots and return the largest error on a grid of 2,001 points.

## Hints

1. Slopes: `np.diff(values) / np.diff(knots)`.
2. Output weights: the first slope, then `np.diff(slopes)`.
3. `c = values[0]`.
